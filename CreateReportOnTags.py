import configparser
import sys
import os


def get_configuration_file():
    config = configparser.ConfigParser()

    # sandbox_configuration_path = sys.path[0] + '\ConfigurationFile.ini'
    # config.read(sandbox_configuration_path)

    # print(sandbox_configuration_path)

    live_configuration_path = sys.executable.replace("CreateReportOnTags.exe","ConfigurationFile.ini")
    config.read(live_configuration_path)

    default_setting = config["DEFAULT"]

    folder_file_location = default_setting["folder_file_location"]
    file_extension = default_setting["file_extension"]
    text_for_counting = default_setting["text_for_counting"]
    log_file_location = default_setting["log_file_location"]

    return folder_file_location, file_extension, text_for_counting, log_file_location


def get_files_directory(folder_file_location, file_extension):
    xml_file_list = []

    for dir_path, dir_names, file_names in os.walk(folder_file_location):
        for file_name in [f for f in file_names if f.endswith(file_extension)]:
            xml_file_list.append(os.path.join(dir_path, file_name))
    return xml_file_list


def count_tag_occurrence(xml_file_list, text_for_counting, log_file_location):
    log_file = open(log_file_location, mode="w+")
    for xml_file in xml_file_list:
        search_file = open(xml_file, "r", encoding="utf8")
        counter = 0

        for line in search_file:
            if text_for_counting in line:
                counter += 1

        log_file.write(str(os.path.basename(xml_file)) + "\t" + str(counter) + "\r")
        print(f"filename: {os.path.basename(xml_file)} counter: {counter}")
        search_file.close()

    log_file.close()


def main():
    try:
        folder_file_location, file_extension, text_for_counting, log_file_location = get_configuration_file()
        # print(f"folder:{folder_file_location}, file:{file_extension}, text:{text_for_counting}")

        print(f"Generating report from {folder_file_location}.")
        xml_file_list = get_files_directory(folder_file_location, file_extension)

        count_tag_occurrence(xml_file_list, text_for_counting, log_file_location)
        print(f"Successful generated log report at {log_file_location}")

    except Exception as e:
        print(f"Error: {e}")


main()
