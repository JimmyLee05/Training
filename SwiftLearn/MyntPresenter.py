 import Foundation

 extension MyntInfoViewController: MYNTKitDelegate {

 	func initMyntListener() {
 		MYNTKit.shared.addMyntKitDelegate(key: selfKey, delegate: self)
 	}

 	
 }