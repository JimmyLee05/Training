import Foundation
import SlightechKit

extension CustomerCareKit {
	
	class func open(_ viewController: UIViewController) {
		if isInJapan {
			if let url = URL(string: "mailto:\(japanServer)") {
				UIApplication.shared.openURL(url)
			}
			return
		}
		//客服组织定制
		var params = [String: String]()
		params["昵称:"] ?= MYNTKit.shared.user?.userName
		params["邮箱:"] ?= MYNTKit.shared.user?.email.lowercased()
		params["用户标识符:"] ?= MYNTKit.shared.user?.alias
		params["设备序列号:"] ?= MYNTKit.shared.mynts.map({$0.sn}).joined(separator: ",")
		params["运营商:"] ?= UIDevice.carrierName
		params["当前国家:"] ?= Locale.current.regionName
		params["手机品牌"] ?= " Apple"
		params["手机型号"] ?= UIDevice.modelName
		params["手机系统"] ?= UIDevice.current.systemName + " " + UIDevice.current.systemVersion
		if UIApplication.isJailbroken {
			params["越狱情况:"] = "已越狱"
		}
		Toast.show(message: NSLocalizedString("LOGIN_ING", comment: "登录中..."))
		SCUser.customerService(success: { userid in
			CustomerCareKit.sharedInstance().login(userid, password: "12345") { error in
				if error == nil {
					CustomerCareKit.sharedInstance().start(viewController, params: params)
				} else {
					Toast.show(message: error?.localizedDescription)
				}
			}
		}) {_, message in
			Toast.show(message: message)
		}
 	}
}
