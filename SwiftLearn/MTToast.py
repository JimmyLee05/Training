import UIKit

class MTToast: NSObject {
	
	class func show(_ message: String?){
		if let message = message {
			Toast.show(title: nil, message: message)
		}
	}
}