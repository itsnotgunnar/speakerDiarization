import sys

topGPT_videos = Videos("topGPT")

topGPT_video_dict = {
        "girl-interview": "https://www.youtube.com/watch?v=HZ6FhDfa9UY",
        "destroyed-woman": "https://www.youtube.com/watch?v=DgRV3F_7BdQ",
        "funny-takes": "https://www.youtube.com/watch?v=DgRV3F_7BdQ",
        "how-to-rich": "https://www.youtube.com/watch?v=U5ylEzE9ktU",
        "destroys-feminist":"https://www.youtube.com/watch?v=AzKH0DCNowQ",
        "sexist": "https://www.youtube.com/watch?v=gexkQ8Y2G80",
        "best-podcast-moments": "https://www.youtube.com/watch?v=GOWFsme5u9E",
        "motivation": "https://www.youtube.com/watch?v=BX1WpL2VlhM",
        "quotes": "https://www.youtube.com/watch?v=lh4_41qpKUk",
        "top-lessons":"https://www.youtube.com/watch?v=EJcRcj5vBj8",
        "advice": "https://www.youtube.com/watch?v=3mBhMdthw-A",
        "women-cheat": "https://www.youtube.com/watch?v=aaXVVgOIpJM",
        "tiktok": "https://www.youtube.com/watch?v=TM7PWLBoh_o",
        "funniest":  "https://www.youtube.com/watch?v=yvRB0inZdWE",
        "toxic": "https://www.youtube.com/watch?v=G_D4r-24bgQ",
        "reinvent": "https://www.youtube.com/watch?v=kQCTfEphctc",
        "podcast-2": "https://www.youtube.com/watch?v=M3vw7-COfGA",
        "coldest": "https://www.youtube.com/watch?v=nbwHftL2-98",
        "piers-morgan": "https://www.youtube.com/watch?v=c1Whpnq1dAY",
        "top-g": "https://www.youtube.com/watch?v=6VFn-1oJqlk",
        "spitting-facts": "https://www.youtube.com/watch?v=-Ol2qiB9tdY",
        "most-savage": "https://www.youtube.com/watch?v=RatbWBeA6Fk",
        "brokies": "https://www.youtube.com/watch?v=IwPKg2kLkrg",
        "coldest-p2": "https://www.youtube.com/watch?v=gpRYrV_YMps",
        "islamic-faith": "https://www.youtube.com/watch?v=YzL_cRdba5k",
        "male-advice": "https://www.youtube.com/watch?v=Gp2PwNcj2x4",
        "inferior":"https://www.youtube.com/watch?v=U5ylEzE9ktU",
        "speeches": "https://www.youtube.com/watch?v=Uw37yw1ZuEI",
        "trolls-feminist": "https://www.youtube.com/watch?v=d4kAPWBH3e8",
        "why-muslim": "https://www.youtube.com/watch?v=vnTiTg0Ouhs",
        "weak-men": "https://www.youtube.com/watch?v=HtoxRMxb7yE",
        "long-patrick": "https://www.youtube.com/watch?v=ZfuSRR1jf1o"
    }

for key in topGPT_video_dict.keys():
    topGPT_videos.add_link(key, topGPT_video_dict[key])

print(topGPT_videos.get_links())