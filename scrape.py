from bs4 import BeautifulSoup
import requests
import json

from segment import Segment


url = 'https://theinfosphere.org/Transcript:Space_Pilot_3000'
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")
transcript = soup.find("div", {"class": "mw-parser-output"})
sections = transcript.find_all("div", {"class": "poem"});

def parse_time(time_id):
    return time_id[len('time-'):].split('-')

def get_segments():
    segments = []
    last_time = [0, 0]
    for section in sections:
        if not (section.p.span):
            print("WARNING: Section without timestamp.")
            print("SKIPPING SEGMENT")
            print(section.p)
            print("CONTINUING")
            continue
        
        new_time = parse_time(section.p.span['id'])
        speaker = section.p.b.text
        
        speaker_section = section.p.find('b')
        speaker_section.extract()
        
        print("SECTION: " + section.p.span['id'])
        time_section = section.p.span
        time_section.extract()
        
        # TODO: ???? i forgor
        cleaned_text = section.p.text.rstrip()[2:]
        segment = Segment(speaker, cleaned_text, last_time[0], last_time[1], new_time[0], str(int(new_time[1])-1))
        segments.append(segment) 
        last_time = new_time

        print("SEGMENT: " + str(segment))
        
    return segments

segments = get_segments()
with open("seg_out.json", "w+") as f:
    f.write(json.dumps(segments, default=(lambda x: x.__dict__ )))
    #for segment in segments:
    #    f.write(json.dumps(segment.__dict__))
print("Output saved to seg_out.json")