import os
import simulation_properties as SP
import introduce_content as IC

#########################################

def get_content_level ():
    return content_level

#########################################

def introduce_all_content (Gcomplete, content_count):

    event_forest = []

    for i in range(content_count):
        content_level = get_content_level()
        event_tree = IC.introduce_content (Gcomplete, content_level)
        event_forest.append(event_tree)

    return event_forest

#########################################

def main():
    event_forest = introduce_all_content (Gcomplete, SP.CONTENT_COUNT)
    return

#########################################

if __name__ = "__main__":
    main()

#########################################
