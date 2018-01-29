"""Modified for NewPCT by PB"""

import sys
import logging
import re
from torrench.utilities.Common import Common


class NewPCT(Common):
    """
    NewPCT class.

    This class fetches results from
    newpct.com and displays
    results in tabular form.
    """

    def __init__(self, title, page_limit):
        """Initialisations."""
        Common.__init__(self)
        self.title = title
        self.logger = logging.getLogger('log1')
        self.index = 0
        self.mylist = []
        self.masterlist = []
        self.urllist = []
        self.url = "http://www.newpct.com/buscar"
        self.headers = ['NAME', 'INDEX', 'SIZE', 'MORE','ADDED']
        self.mapper = []
        self.soup = None
        self.pages = page_limit
        self.total_fetch_time = 0
        self.soup_dict = {}
        self.class_name = self.__class__.__name__.lower()

    def get_html(self, url, isMoreDetails=False):
        """
        Get HTML content

        Make a POST request to '/buscar' for each page and grab results
        """
        try:
            for self.page in range(self.pages):
                print("\nFetching from page: %d" % (self.page+1))

                if isMoreDetails:
                    # More details
                    query_page = '/pg/'+ str(self.page) if self.page != 0 else ''
                    self.soup, time = self.http_request_time(url + query_page)
                else:
                    # Search
                    query_page = self.page if self.page != 0 else None
                    self.soup, time = self.http_request_time(url, False, { "q" : self.title, "pg" : query_page } )

                results = self.soup.find('ul', 'buscar-list').find_all('li')
                if results is None:
                    print("[No results]")
                    break
                self.logger.debug("fetching page %d/%d" % (self.page+1, self.pages))                
                print("[in %.2f sec]" % (time))
                self.logger.debug("page fetched in %.2f sec!" % (time))
                self.total_fetch_time += time
                self.soup_dict[self.page] = self.soup
        except Exception as e:
            self.logger.exception(e)
            print("Error message: %s" %(e))
            print("Something went wrong! See logs for details. Exiting!")
            sys.exit(2)


    def parse_html(self):
        """
        Parse HTML to get required results.

        Results are fetched in masterlist list.
        """
        try:
            for page in self.soup_dict:
                self.soup = self.soup_dict[page]
                results = self.soup.find('ul', 'buscar-list').find_all('li')
                for item in results:
                    try:
                        url = item.a['href']
                        has_more_info = "http://www.newpct.com/serie" in url
                        has_more_info_indicator = self.colorify("red", '>>>') if has_more_info else self.colorify("green", '-')
                        name = item.h2.text
                        data = item.div.find_all('span', class_=False, id=False, recursive=False)
                        date = data[0].text
                        size = data[1].text
                        self.index += 1
                        self.mapper.insert(self.index, (name, url, has_more_info))
                        self.mylist = [name, "--" + str(self.index) + "--", size, has_more_info_indicator , date]
                        self.masterlist.append(self.mylist)
                        self.urllist.append(url)
                    except AttributeError as e:
                        self.logger.exception(e)
                        pass
        except Exception as e:
            self.logger.exception(e)
            print("Error message: %s" % (e))
            print("Something went wrong! See logs for details. Exiting!")
            sys.exit(2)
            
    def select_option(self, index):
        """
        Select option method.

        If the result is a TVShow it will show first the episode list.
        """
        url = self.mapper[index-1][1]
        has_more_info = self.mapper[index-1][2]
        if has_more_info:
            #Is a TVShow and a new selection is required
            #Keep old results
            old_masterList = self.masterlist
            old_mapper = self.mapper
            old_index = self.index
            self.masterlist = []
            self.mapper = []
            self.index = 0

            self.get_html(url, True)
            self.parse_html()
            self.post_fetch()

            #Recover old results
            self.masterlist = old_masterList
            self.mapper = old_mapper
            self.index = old_index
        else:
            #Normal download, can use super
            super().select_option(index)

    def get_links(self, index):
        """
        Get links method.

        This method fetches and returns magnetic/upstream links.
        """
        try:
            url = self.mapper[index-1][1]
            download_soup, time = self.http_request_time(url)
            download_url = re.search("window.location.href = \"(.*)\";", str(download_soup)).group(1)
            return download_url, download_url
        except Exception as e:
            print("Something went wrong. See logs for details.")
            self.logger.exception(e)


def main(title, page_limit = 1):
    """Execution begins here."""
    try:
        print("\n[NewPCT]\n")
        title = title.lower()
        dw = NewPCT(title, page_limit)
        print("Fetching results...")
        dw.get_html(dw.url)
        dw.parse_html()
        dw.post_fetch()
        print("\nBye!")
        # dw.select_torrent()
    except KeyboardInterrupt:
        tpb.logger.debug("Keyboard interupt! Exiting!")
        print("\n\nAborted!")

if __name__ == "__main__":
    print("Its a module!")
