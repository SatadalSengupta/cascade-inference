import os
import generate_graphs as GG
import simulation_properties as SP
import introduce_content as IC
import random

#########################################

def get_content_level (levels):
    content_level = random.randint(1,levels)
    return content_level

#########################################

def introduce_all_content (Gcomplete, content_count):

    EF = []

    for i in range(content_count):
        content_level = get_content_level(SP.CONTENT_LEVELS)
        EFlocal = IC.introduce_content (Gcomplete, content_level)
        EF.extend(EFlocal)

    return EF

#########################################

def main():
    Gbase, Gcomplete = GG.generate_graphs(SP.SAMPLE_SIZE,SP.MEAN,SP.SD,SP.VIEW_BOOST,SP.SHARE_BOOST)
    EF = introduce_all_content (Gcomplete, SP.CONTENT_COUNT)
    #print len(EF)
    return

#########################################

if __name__ == "__main__":
    main()

#########################################
