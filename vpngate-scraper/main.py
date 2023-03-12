from Scraper.vpn_gate_scraper import VpnGateScraper

if __name__ == '__main__':
    scraper = VpnGateScraper()
    
    ovpn_files = scraper.scrape_ovpn_files(10)
    
    