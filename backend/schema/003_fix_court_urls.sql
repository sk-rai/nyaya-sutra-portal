-- Fix AFT Delhi cause list URL (was incorrectly pointing to Mumbai)
UPDATE courts
SET cause_list_url = 'https://aftdelhi.nic.in/index.php/case-mgmt/daily-cause-list'
WHERE code = 'aft_del';

-- Update AFT Mumbai URL
UPDATE courts
SET cause_list_url = 'https://aftdelhi.nic.in/index.php/reg-benches/mumbai/mumbai-cause-list'
WHERE code = 'aft_mum';

-- Update scraper keys to use the generic scraper
UPDATE courts SET scraper_key = 'aft_generic' WHERE court_type = 'aft' AND scraper_key IS NULL;
UPDATE courts SET scraper_key = 'cat_generic' WHERE court_type = 'cat' AND scraper_key IS NULL;
