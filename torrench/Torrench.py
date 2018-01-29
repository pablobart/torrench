"""Torrench Module."""

import argparse
import logging
import os
import sys

from torrench.utilities.Config import Config


class Torrench(Config):
    """
    Torrench class.

    This class resolves input arguments.
    Following arguments are present -

    optional arguments:
        -h, --help            show this help message and exit
        -v, --version         Display version and exit.
        -C, --cross_site      Enable cross-site search
        -U, --update-config   Update config.ini file.
        --interactive         Enable interactive mode for searches
        --no-merge            (Cross-site) Do not merge results in one table
        --sorted              (Cross-site) sort results on basis of Seeds.

    Main Sites:
        search                Search LinuxTracker (default)
        -d, --distrowatch     Search Distrowatch

    Optional Sites:
    Requires configuration (disabled by default)

        -t, --thepiratebay    Search thepiratebay (TPB)
        -k, --kickasstorrent  Search KickassTorrent (KAT)
        -s, --skytorrents     Search SkyTorrents
        -x, --x1337           Search 1337x
        -r, --rarbg           Search RarBg
        -n, --nyaa            Search Nyaa
        -l, --limetorrents    Search LimeTorrents
        -i, --idope           Search Idope
        -b, --xbit            Search XBit.pw
        -g, --libgen          Search LibGen (Ebooks)
        -npct, --newpct       Search NewPCT

    Additional options:
        -c, --clear-html      Clear all [TPB] torrent description HTML files and exit.
        -p LIMIT, --page-limit LIMIT
                                Number of pages to fetch results from. [default: 1]
        --copy                Copy magnetic link to clipboard
        --top                 Get TOP torrents [TPB/SkyTorrents]
    """

    def __init__(self):
        """Initialisations."""
        Config.__init__(self)
        self.__version__ = "Torrench (1.0.61)"
        self.logger = logging.getLogger('log1')
        self.args = None
        self.input_title = None
        self.page_limit = 0
        self.module_args = []

    def define_args(self):
        """All input arguments are defined here."""
        self.logger.debug("command-input: %s" % (sys.argv))
        parser = argparse.ArgumentParser(description="A Simple Command-line torrent search program.")
        main_sites = parser.add_argument_group("Main Sites")
        optional_sites = parser.add_argument_group("Optional Sites", "Requires configuration (disabled by default)")
        misc = parser.add_argument_group("Additional options")
        main_sites.add_argument("search",
                            help="Search LinuxTracker (default)",
                            nargs="?",
                            default=None)
        main_sites.add_argument("-d",
                            "--distrowatch",
                            action="store_true",
                            help="Search Distrowatch")
        optional_sites.add_argument("-t",
                            "--thepiratebay",
                            action="store_true",
                            help="Search thepiratebay (TPB)")
        optional_sites.add_argument("-k",
                            "--kickasstorrent",
                            action="store_true",
                            help="Search KickassTorrent (KAT)")
        optional_sites.add_argument("-s",
                            "--skytorrents",
                            action="store_true",
                            help="Search SkyTorrents")
        optional_sites.add_argument("-x",
                            "--x1337",
                            action="store_true",
                            help="Search 1337x")
        optional_sites.add_argument("-r",
                            "--rarbg",
                            action="store_true",
                            help="Search RarBg")
        optional_sites.add_argument("-n",
                            "--nyaa",
                            action="store_true",
                            help="Search Nyaa")
        optional_sites.add_argument("-l",
                            "--limetorrents",
                            action="store_true",
                            help="Search LimeTorrents")
        optional_sites.add_argument("-i",
                            "--idope",
                            action="store_true",
                            help="Search Idope")
        optional_sites.add_argument("-b",
                            "--xbit",
                            action="store_true",
                            help="Search XBit.pw")
        optional_sites.add_argument("-g",
                            "--libgen",
                            action="store_true",
                            help="Search LibGen (Ebooks)")
        optional_sites.add_argument("-npct",
                            "--newpct",
                            action="store_true",
                            help="Search NewPCT")
        misc.add_argument("-c",
                            "--clear-html",
                            action="store_true",
                            default=False,
                            help="Clear all [TPB] torrent description HTML files and exit.")
        misc.add_argument("-p",
                            "--page-limit",
                            type=int,
                            help="Number of pages to fetch results from. [default: 1]",
                            default=1,
                            dest="limit")
        misc.add_argument("--copy",
                            action="store_true",
                            default=False,
                            help="Copy magnetic link to clipboard")
        misc.add_argument("--top",
                            action="store_true",
                            default=False,
                            help="Get TOP torrents [TPB/SkyTorrents]")
        parser.add_argument("-v",
                            "--version",
                            action='version',
                            version=self.__version__,
                            help="Display version and exit.")
        parser.add_argument("-C",
                            "--cross_site",
                            default=False,
                            action="store_true",
                            help="Enable cross-site search")
        parser.add_argument("-U",
                            "--update-config",
                            action="store_true",
                            default=False,
                            help="Update config.ini file.")
        parser.add_argument("--interactive",
                            default=False,
                            action="store_true",
                            help="Enable interactive mode for searches")
        parser.add_argument("--no-merge",
                            default=False,
                            action="store_true",
                            help="(Cross-site) Do not merge results in one table")
        parser.add_argument("--sorted",
                            default=False,
                            action="store_true",
                            help="(Cross-site) sort results on basis of Seeds.")

        self.args = parser.parse_args()

    def check_copy(self):
        """Check if --copy argument is present."""
        self.define_args()
        if self.args.copy:
            return True

    def remove_temp_files(self):
        """
        To remove TPB HTML files (-c).

        Clearing HTML files only works for TPB (-t)
        (since only TPB generates HTML for torrent descriptions)
        Default location for temp files is
        ~/.torrench/temp (Windows/linux)
        """
        self.logger.debug("Selected -c :: remove tpb temp html files.")
        home = os.path.expanduser(os.path.join('~', '.torrench'))
        temp_dir = os.path.join(home, "temp")
        self.logger.debug("temp directory default location: %s" % (temp_dir))
        if not os.path.exists(temp_dir):
            print("Directory not initialised. Exiting!")
            self.logger.debug("directory not found")
            sys.exit(2)
        files = os.listdir(temp_dir)
        if not files:
            print("Directory empty. Nothing to remove")
            self.logger.debug("Directory empty!")
            sys.exit(2)
        else:
            for count, file_name in enumerate(files, 1):
                os.remove(os.path.join(temp_dir, file_name))
            print("Removed {} file(s).".format(count))
            self.logger.debug("Removed {} file(s).".format(count))
            sys.exit(2)

    def verify_input(self):
        """To verify if input given is valid or not."""
        if self.input_title is None and not self.args.interactive:
            self.logger.debug("Bad input! Input string expected! Got 'None'")
            print("\nInput string expected.\nUse --help for more\n")
            sys.exit(2)

        if self.page_limit <= 0 or self.page_limit > 50:
            self.logger.debug("Invalid page_limit entered: %d" % (tr.page_limit))
            print("Enter valid page input [0<p<=50]")
            sys.exit(2)

    def resolve_args(self):
        """Resolve input arguments."""
        _PRIVATE_MODULES = (
            self.args.thepiratebay,
            self.args.kickasstorrent,
            self.args.skytorrents,
            self.args.rarbg,
            self.args.x1337,
            self.args.nyaa,
            self.args.idope,
            self.args.xbit,
            self.args.libgen,
            self.args.limetorrents,
            self.args.newpct
        )  # These modules are only enabled through manual configuration.
        if self.args.clear_html:
            if not self.args.thepiratebay:
                print("error: use -c with -t")
                sys.exit(2)
            else:
                self.remove_temp_files()

        if any(_PRIVATE_MODULES):
            if not self.file_exists():
                print("\nConfig file not configured. Configure to continue. Read docs for more info.")
                print("Config file either does not exist or is not enabled! Exiting!\n")
                sys.exit(2)
            else:
                if self.args.thepiratebay:
                    self.logger.debug("using thepiratebay")
                    if self.args.top:
                        self.logger.debug("selected TPB TOP-torrents")
                        self.input_title = None
                        self.page_limit = None
                    self.logger.debug("Input title: [%s] ; page_limit: [%s]" % (self.input_title, self.page_limit))
                    import torrench.modules.thepiratebay as tpb
                    tpb.main(self.input_title, self.page_limit)
                elif self.args.kickasstorrent:
                    self.logger.debug("Using kickasstorrents")
                    self.logger.debug("Input title: [%s] ; page_limit: [%s]" % (self.input_title, self.page_limit))
                    import torrench.modules.kickasstorrent as kat
                    kat.main(self.input_title, self.page_limit)
                elif self.args.skytorrents:
                    self.logger.debug("Using skytorrents")
                    if self.args.top:
                        self.logger.debug("selected SkyTorrents TOP-torrents")
                        self.input_title = None
                        self.page_limit = None
                    self.logger.debug("Input title: [%s] ; page_limit: [%s]" % (self.input_title, self.page_limit))
                    import torrench.modules.skytorrents as sky
                    sky.main(self.input_title, self.page_limit)
                elif self.args.nyaa:
                    self.logger.debug("Using Nyaa.si")
                    import torrench.modules.nyaa as nyaa
                    nyaa.main(self.input_title, self.page_limit)
                elif self.args.xbit:
                    self.logger.debug("Using XBit.pw")
                    self.logger.debug("Input title: [%s]" % (self.input_title))
                    import torrench.modules.xbit as xbit
                    xbit.main(self.input_title)
                elif self.args.rarbg:
                    self.logger.debug("Using RarBg")
                    self.logger.debug("Input title: [%s]" % (self.input_title))
                    import torrench.modules.rarbg as rbg
                    rbg.main(self.input_title)
                elif self.args.x1337:
                    self.logger.debug("Using 1337x")
                    self.logger.debug("Input title: [%s] ; page_limit: [%s]" % (self.input_title, self.page_limit))
                    import torrench.modules.x1337 as x13
                    x13.main(self.input_title, self.page_limit)
                elif self.args.limetorrents:
                    self.logger.debug("Using LimeTorrents")
                    self.logger.debug("Input title: [%s] ; page_limit: [%s]" % (self.input_title, self.page_limit))
                    import torrench.modules.limetorrents as lmt
                    lmt.main(self.input_title, self.page_limit)
                elif self.args.idope:
                    self.logger.debug("Using Idope")
                    self.logger.debug("Input title: [%s] ; page_limit: [%s]" % (self.input_title, self.page_limit))
                    import torrench.modules.idope as idp
                    idp.main(self.input_title, self.page_limit)
                elif self.args.libgen:
                    self.logger.debug("Using LibGen")
                    self.logger.debug("Input ISBN: [%s]" % (self.input_title))
                    import torrench.modules.libgen as libg
                    libg.main(self.input_title)
                elif self.args.newpct:
                    self.logger.debug("Using NewPCT")
                    self.logger.debug("Input title: [%s] ; page_limit: [%s]" % (self.input_title, self.page_limit))
                    import torrench.modules.newpct as newpct
                    newpct.main(self.input_title, self.page_limit)
        elif self.args.distrowatch:
            self.logger.debug("Using distrowatch")
            self.logger.debug("Input title: [%s]" % (self.input_title))
            import torrench.modules.distrowatch as distrowatch
            distrowatch.main(self.input_title)
        elif self.args.interactive:
            self.logger.debug("Using interactive mode")
            import torrench.utilities.interactive as interactive
            interactive.inter()
        else:
            self.logger.debug("Using linuxtracker")
            self.logger.debug("Input title: [%s]" % (self.input_title))
            import torrench.modules.linuxtracker as linuxtracker
            linuxtracker.main(self.input_title)


def main():
    """Execution begins here."""
    try:
        tr = Torrench()
        tr.define_args()
        if tr.args.update_config:
            import torrench.utilities.update_config as update
            update.main()
            sys.exit(2)
        if tr.args.cross_site:
            tr.logger.debug("Using cross-site")
            import torrench.utilities.cross_site as cs
            cs.main(tr.args)
        else:
            if tr.args.top:
                if tr.args.thepiratebay or tr.args.skytorrents:
                    tr.resolve_args()
                else:
                    print("error: --top is only supported with -t/-s")
                    sys.exit(2)
            else:
                tr.input_title = tr.args.search
                tr.page_limit = tr.args.limit
                if not tr.args.clear_html and not tr.args.interactive:
                    tr.verify_input()
                    tr.input_title = tr.input_title.replace("'", "")
                tr.resolve_args()
    except KeyboardInterrupt as e:
        tr.logger.debug("Keyboard interupt! Exiting!")
        print("\n\nAborted!")


if __name__ == '__main__':
    main()
