import xml.etree.ElementTree as ET
#!/usr/bin/env python
# -*- coding: latin1 -*-

import re
import itertools
import codecs


input_estc = "estc.xml"

def estc_xml2csv(filename):

    datafield_exists = False
    br = False

    counter = 0
    writefile = open(filename.replace(".xml",".csv"), "w")
    
    with open(filename, "r") as f:
        writefile.write("Record_seq\tField_seq\tSubfield_seq\tField_code\tSubfield_code\tValue\n")
        for l in f:
            if l.startswith("<marc:record>"):
                counter = counter + 1
                tmpCodes = {}
                fieldvalue = re.search("<marc:leader>([^<]*)<[/]marc:", l).groups()[0]
                tmpCodes["leader"] = fieldvalue
                datafield_exists = True
                tmpCodes["leader"] = fieldvalue
                tmpCodes["leader_record_status_05"] = fieldvalue[5]
                tmpCodes["leader_material_type_06"] = fieldvalue[6]
                tmpCodes["leader_bibliographical_level_07"] = fieldvalue[7]
                tmpCodes["leader_control_type_08"] = fieldvalue[8]
                tmpCodes["leader_coding_scheme"] = fieldvalue[9]
                if len(fieldvalue) >= 18:
                    tmpCodes["leader_encoding_level_17"] = fieldvalue[17]
                    tmpCodes["leader_descriptive_catalog_18"] = fieldvalue[18]
                    tmpCodes["leader_multipart_19"] = fieldvalue[19]
                tuntematon_kalalaji=False
                if fieldvalue[6:8] in ("ab", "ai", "as"):
                    fieldtype008 = "series"
                elif (fieldvalue[6:8] in ("aa", "ac", "ad", "am", "ae", "af", "ag")) or \
                     (fieldvalue[6] == "t"):
                    # ae, af, ag undocumented. af & ag simply guessed as books
                    fieldtype008 = "books"
                elif fieldvalue[6] in ("e", "f"):
                    fieldtype008 = "maps"
                elif fieldvalue[6] in ("c", "d", "e", "j"):
                    fieldtype008 = "music"
                elif fieldvalue[6] in ("g", "k", "o", "r"):
                    fieldtype008 = "visual"
                elif fieldvalue[6] == "m":
                    fieldtype008 = "files"
                elif fieldvalue[6] == "p":
                    fieldtype008 = "mixed"
                else:
                    fieldtype008 = ""
                    print "Unknown field type:", fieldvalue[6:8]
                    print(fieldvalue)
                    tuntematon_kalalaji=True
                
                tmpCodes["leader"] = fieldvalue
                for key, value in tmpCodes.items():
                    writefile.write(str(counter) + "\t" + \
                                    "1" + "\t" + \
                                    "1" + "\t" + \
                                    "leader" + "\t" +\
                                    key + "\t" + \
                                    value + \
                                    "\n")
                writefile.write(str(counter) + "\t" + \
                                "1" + "\t" + \
                                "1" + "\t" + \
                                "leader_raw" + "\t" + \
                                "" + "\t" + \
                                fieldvalue + \
                                "\n")
                
            elif l.startswith("<marc:controlfield"):
                fields = re.split("(<marc:[^<]+<[\/]marc[^>]+>)", l)
                datafield_exists = False
                for field in fields:
                    if field == "":
                        pass
                    
                        
                    elif field.startswith("<marc:controlfield"):
                        fieldcode = re.search("tag=\"([0-9]+)\"", field).groups()[0]
                        fieldvalue = re.search(">([^<]+)<", field).groups()[0]

                        if fieldcode == "008":
                            tmpCodes = {}
                            tmpCodes["entered_date_008"] = fieldvalue[:6]
                            if (len(fieldvalue) >= 7):
                                tmpCodes["publication_type_008"] = fieldvalue[6]
                            if (len(fieldvalue) >= 11):
                                tmpCodes["year1_008"] = fieldvalue[7:11]
                            if (len(fieldvalue) >= 15):
                                tmpCodes["year2_008"] = fieldvalue[11:15]
                            if (len(fieldvalue) >= 18):
                                tmpCodes["publication_place_008"] = fieldvalue[15:18]
                            if (len(fieldvalue) >= 38):
                                tmpCodes["language_008"] = fieldvalue[35:38]
                                lang008 = fieldvalue[35:38]
                            if (len(fieldvalue) >= 39):
                                tmpCodes["modified_record_008"] = fieldvalue[38]
                            if (len(fieldvalue) >= 40):
                                tmpCodes["cataloging_source_008"] = fieldvalue[39]

                            if (len(fieldvalue) < 35):
                                continue
                            if (fieldtype008 == "series"):
                                tmpCodes["frequency_008series"] = fieldvalue[18]
                                tmpCodes["resource_type_008series"] = fieldvalue[21]
                                tmpCodes["form_of_original_008series"] = fieldvalue[22]
                                tmpCodes["form_of_item_008series"] = fieldvalue[23]
                                tmpCodes["nature_of_work_008series"] = fieldvalue[24]
                                tmpCodes["nature_of_contents_008series"] = fieldvalue[25:28]
                                tmpCodes["government_publications_008series"] = fieldvalue[28]
                                tmpCodes["conference_publication_008series"] = fieldvalue[29]
                                tmpCodes["original_script_008series"] = fieldvalue[33]
                                tmpCodes["entry_convention_008series"] = fieldvalue[34]
                            elif (fieldtype008 == "books"):
                                tmpCodes["illustrations_008books"] = fieldvalue[18:22]
                                tmpCodes["target_audience_008books"] = fieldvalue[22]
                                tmpCodes["form_of_item_008books"] = fieldvalue[23]
                                tmpCodes["nature_of_contents_008books"] = fieldvalue[24:28]
                                tmpCodes["government_publications_008books"] = fieldvalue[28]
                                tmpCodes["conference_publication_008books"] = fieldvalue[29]
                                tmpCodes["festchrift_008books"] = fieldvalue[30]
                                tmpCodes["index_008books"] = fieldvalue[31]
                                tmpCodes["literary_form_008books"] = fieldvalue[33]
                                tmpCodes["biography_008books"] = fieldvalue[34]
                            elif (fieldtype008 == "maps"):
                                tmpCodes["relief_008maps"] = fieldvalue[18:22]
                                tmpCodes["projection_008maps"] = fieldvalue[22:24]
                                tmpCodes["cartographic_material_type_008maps"] = fieldvalue[25]
                                tmpCodes["government_publications_008maps"] = fieldvalue[28]
                                tmpCodes["conference_publication_008maps"] = fieldvalue[29]
                                tmpCodes["index_008maps"] = fieldvalue[31]
                                tmpCodes["special_format_characteristics_008maps"] = fieldvalue[33:35]
                            elif (fieldtype008 == "music"):
                                tmpCodes["composition_format_008music"] = fieldvalue[18:20]
                                tmpCodes["score_format_008music"] = fieldvalue[20]
                                tmpCodes["music_parts_008music"] = fieldvalue[21]
                                tmpCodes["target_audience_008music"] = fieldvalue[22]
                                tmpCodes["form_of_item_008music"] = fieldvalue[23]
                                tmpCodes["accompanying_matter_008music"] = fieldvalue[24:30]
                                tmpCodes["text_recordings_008music"] = fieldvalue[30:32]
                                tmpCodes["transposition_arrangement_008music"] = fieldvalue[33]
                            elif (fieldtype008 == "visual"):
                                tmpCodes["running_time_008visual"] = fieldvalue[18:21]
                                tmpCodes["target_audience_008visual"] = fieldvalue[22]
                                tmpCodes["government_publications_008visual"] = fieldvalue[28]
                                tmpCodes["conference_publication_008visual"] = fieldvalue[29]
                                tmpCodes["type_of_material_008visual"] = fieldvalue[33]
                                tmpCodes["technique_008visual"] = fieldvalue[34]
                            elif (fieldtype008 == "files"):
                                tmpCodes["target_audience_008files"] = fieldvalue[22]
                                tmpCodes["form_of_item_008files"] = fieldvalue[23]
                                tmpCodes["type_of_file_008files"] = fieldvalue[26]
                                tmpCodes["government_publications_008files"] = fieldvalue[28]
                                tmpCodes["conference_publication_008files"] = fieldvalue[29]
                            elif (fieldtype008 == "mixed"):
                                tmpCodes["form_of_item_008mixed"] = fieldvalue[23]
                            
                            for key, value in tmpCodes.items():
                                if re.search("^ *[\|]* *$", value) == None:
                                    writefile.write(str(counter) + "\t" + \
                                                    "1" + "\t" + \
                                                    "1" + "\t" + \
                                                    "008" + "\t" + \
                                                    key + "\t" + \
                                                    value + \
                                                    "\n")
                            writefile.write(str(counter) + "\t" + \
                                            "1" + "\t" + \
                                            "1" + "\t" + \
                                            "008_raw" + "\t" + \
                                            "" + "\t" + \
                                            fieldvalue + \
                                            "\n")
                            
                    elif "<marc:datafield" in field:
                        datafield_exists = True
                        tag = re.search("tag=\"([0-9]+)\"", field).groups()[0]
                        ind1 = re.search("ind1=\"([^\"]*)\"", field).groups()[0]
                        if tag in tmpCodes.keys():
                            prevvalue = tmpCodes.pop(tag)
                            field_seq = prevvalue + 1
                        else:
                            field_seq = 1
                        tmpCodes[tag] = field_seq
                        
                        if ind1 != "" and ind1 != " " and ind1 != "#":
                            fieldcode = tag + "_ind1"
                            if fieldcode in tmpCodes.keys():
                                prevvalue = tmpCodes.pop(fieldcode)
                                seq = prevvalue + 1
                            else:
                                seq = 1
                            tmpCodes[fieldcode] = seq
                            writefile.write(str(counter) + "\t" + \
                                            str(field_seq) + "\t" + \
                                            "1" + "\t" + \
                                            tag + "\t" + \
                                            "ind1" + "\t" + \
                                            ind1 + \
                                            "\n")
                            
                        ind2 = re.search("ind2=\"([^\"]*)\"", field).groups()[0]
                        if ind2 != "" and ind2 != " " and ind2 != "#":
                            fieldcode = tag + "_ind2"
                            if fieldcode in tmpCodes.keys():
                                prevvalue = tmpCodes.pop(fieldcode)
                                seq = prevvalue + 1
                            else:
                                seq = 1
                            tmpCodes[fieldcode] = seq
                            writefile.write(str(counter) + "\t" + \
                                            str(field_seq) + "\t" + \
                                            "1" + "\t" + \
                                            tag + "\t" + \
                                            "ind2" + "\t" + \
                                            ind2 + \
                                            "\n")
                            
                    elif field.startswith("<marc:subfield"):
                        code = ""
                        code = re.search("code=\"([^\"]*)\"", field).groups()[0]
                        fieldcode = tag + code
                        fieldvalue = re.search(">([^<]*)<", field).groups()[0]
                        if fieldcode + str(field_seq) in tmpCodes.keys():
                            prevvalue = tmpCodes.pop(fieldcode + str(field_seq))
                            seq = prevvalue + 1
                        else:
                            seq = 1
                        tmpCodes[fieldcode + str(field_seq)] = seq
                        writefile.write(str(counter) + "\t" + \
                                        str(field_seq) + "\t" +\
                                        str(seq) + "\t" + \
                                        tag + "\t" + \
                                        code + "\t" + \
                                        fieldvalue + \
                                        "\n")
    writefile.close()
