import Foundation

public func MTLocalizedString(_ key: String, comment: String) -> String {
	
	if let string = I18nManager.sharedInstance().bundle?.localizedString(forKey: key,
																		 value: "",
																		 table: nil) {
		return string
	}
	return ""
}

extension I18nManager {
	
	func checkNewVersion() {
		
	}
}