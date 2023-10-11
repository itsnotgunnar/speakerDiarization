class Videos:
    def __init__(self, category):
        self.category = category
        self.links = {}
        self.video_count = self.links.keys().__len__()
    
    def get_links(self):
        return self.links
    
    def get_video_count(self):
        return self.video_count
    
    def get_category(self):
        return self.category
    
    def add_link(self, title, link):
        self.links[title] = link
        self.video_count = self.links.keys().__len__()

    def set_category(self, category):
        self.category = category

    def set_links(self, links):
        self.links = links
        self.video_count = self.links.__len__()

# Path: topGPT/assets/videos/links.py