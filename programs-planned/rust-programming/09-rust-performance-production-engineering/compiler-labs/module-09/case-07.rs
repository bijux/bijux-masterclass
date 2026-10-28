fn main(){ let manifest="artifact=app\nprofile=dist\n"; assert!(!manifest.contains("timestamp")); assert!(!manifest.contains("/home/")); }
