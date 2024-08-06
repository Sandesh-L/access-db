import os
import re

# This code should do three things:
#   find all of the software names
#   Match software name with rp names
#   Match software and rp with available versions

#############
# module spider output will format softwares like so: "  softwarename"
#       2 spaces followed by the name of the software
# In case of nested software (bridges-2) it is formatted like so: "  AI: AI/package_version"

############


#################################################################################
#   get_software_lines                                                          #
#       finds the lines with software names and version from a given `moduel    #
#       spider` output file. Lines with software name and version always start  #
#       with two spaces                                                         #
#   Args:                                                                       #
#       file_path {string}: a string with the full path to the file             #
#    Return:                                                                    #
#        software_lines {list}: A list where each item is a line with with      #
#            software and version info                                          #
#################################################################################
def get_software_lines(file_path):
    with open(file_path) as f:
       file_content = f.read()
    
    file_lines = file_content.split('\n')

    # Find lines with software info (they start with exactly two spaces)
    software_lines = [line.strip() for line in file_lines if re.match(r'^ {2}(?! )', line)] # .strip() to remove the leading two spaces
    
    return software_lines 


#################################################################################
#   get_software_name_and_versions                                              #
#       Finds software name and version info from a given software_line.        #
#       Handles special cases for Kyric software and and versions.              #
#       Handles special cases of Bridges-2 nested softwares                     #
#   Args:                                                                       #
#       software_line {string}: a software line from module spider output.      #
#           returned from the get_software_lines function                       #
#    Return:                                                                    #
#        software_name_and_versions{Dict}: A dictionary of software name and    #
#           versions. Key is the software name and values are the versions.     #
#           Both key and vlaue are strings                                      #
#################################################################################
def get_software_name_and_versions(software_line):

    software_name_and_versions = {}

    split_software_line = software_line.split(':',1)
    software_name = split_software_line[0].lower()
    software_versions = split_software_line[1].lower()

    # Kyric specific: separate the string at `-{0-9}` (a dash followed by a number)
    pattern = r'-(?=\d)'    # regex pattern for a dash followed by a number
    if re.search(pattern, software_name):
        split_software_name = re.split(pattern, software_name)
        software_name = split_software_name[0]
    else:
        software_name = software_name
    
    # software_name is found, double checking version
    
    versions_list = software_versions.split(",")
    versions_str = ""
    for version in versions_list:
        # standard lmod version_info look like this: software/version
        # convert it to only get "version"
        version_info = version.split('/', 1)[-1]
        # print(version_info)
        # check if software is nested (software name is in version info)
        # Bridges-2 specific: version data has `string_number` pattern
        pattern = r'(?<=[a-zA-Z])_(?=\d)'    # regex for string_number pattern
        if re.search(pattern, version_info):    # if pattern is in version_info
            # nested version data found
            nested_software_and_version = re.split(pattern, version_info)
            nested_software = nested_software_and_version[0]
            nested_version = nested_software_and_version[1]

            # check if nested software already exists in software_name_and_versions
            if not nested_software in software_name_and_versions:
                software_name_and_versions[nested_software] = nested_version

            elif not nested_version in software_name_and_versions[nested_software]:
                software_name_and_versions[nested_software] = software_name_and_versions[nested_software] + ", "+ nested_version
        
        # Kyric specific: Kyric doesn't always follow the "software/version" format
        # it sometimes uses "software-version-compiler" format (string-int-string)
        if '/' not in version:
            pattern = r'(?<=[a-zA-Z])-(?=\d)'   # pattern for string-int
            version_comp = re.split(pattern, version)[-1]  # now we have version-compiler only 
            version_info = version_comp.split("-", 1)[0]    # now we have only the version

        if versions_str:    # comma separate if string is not empty
            versions_str += ", " + version_info
        else:
            versions_str = version_info


    # add software name and versions
    # in case of nested softwares, we also want to keep the parent container as a software (for now)
    if not software_name in software_name_and_versions:
        software_name_and_versions[software_name] = versions_str

    elif not nested_version in software_name_and_versions[software_name]:
        software_name_and_versions[software_name] = nested_software_and_version[software_name] + ", "+ versions_str
    
    return software_name_and_versions


#################################################################################
#   parse_spider_output                                                         #
#       prases the output of `module spider`. Associates each rp with it's      #
#       software and versions                                                   #
#   Args:                                                                       #
#      spider_output_dir{string}: path to parent directory of all spider output #
#      files                                                                    #
#   Functions:                                                                  #
#       get_software_lines: for a given spider file path, returns a list of the #
#           lines with software and version info                                #
#       get_software_name_and_versions: Retruns software name and versions      #
#    Return:                                                                    #
#       rp_software_and_versions{Dict}: A dictinory with lowercase rp names as  #
#           the keys. The value is a tuple of strings where the first index is  # 
#           the software name and second is the versions both lowercased        #
#################################################################################
def parse_spider_output(spider_output_dir="./data/spiderOutput"):
    rp_software_and_versions = {}

    for file in os.listdir(spider_output_dir):

        full_file_path = os.path.join(spider_output_dir, file)

        if not os.path.isfile(full_file_path):
            print(f"Item {file} inside {spider_output_dir} is not a file. Skipping")
            continue

        rp_name = file.split('_')[0]    # Find the rp name from the file name
        software_lines = get_software_lines(full_file_path)

        rp_software_and_versions[rp_name] = []

        for software_line in software_lines:
            software_name_and_versions = get_software_name_and_versions(software_line)

            rp_software_and_versions[rp_name] += list(software_name_and_versions.items())

    return rp_software_and_versions