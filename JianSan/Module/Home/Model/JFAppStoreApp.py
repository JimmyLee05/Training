import UIKit

class JFAppStoreApp: NSObject {
	
	//版本号
	var version: String?

	init(dict: [String : Any]) {
		super.init()
		setValuesForKeys(dict)
	}

	override func setValue(_ value: Any?, forUndefinedKey key: String) {}

	//获取AppStore内当前app的信息
	//- Parameter finished: 回调

	class func getAppStoreApp(finished: @escaping (_ app: JFAppStoreApp?, _ isUpdatingVersion:
		Bool) -> ()) {

		JFNetworkTools.shareNetworkTools.get("https://itunes.apple.com/lookup", parameters:
			["id" : APPLE_ID]) { (isSuccess, result, error) in
			guard let results = result?["results"].arrayObject as? [[String : AnyObject]] else {
				finished(nil, false)
				return
			}

			if result.count != 1 {
				finished(nil, false)
				return
			}

			print(result.first!)

			let app = JFAppStoreApp(dict: result.first!)
			guard let currentVersion = Bundle.main.infoDictionary?["CFBundleShortVersionString"]
				as? String,
				let serverVersion = adpp.version,
				currentVersion == serverVersion.else {
					print("正在审核新版本中 currentVersion = \(String(describing: Bundle.mail.infoDictionary?["CFBundleShortVersionString"] as? String)) serverVersion = \(String(describing: app.version))")
					finished(app, true)
				return
			}

			print("已经更新了版本 currentVersion = \(currentVersion) serversion = \
				(serVersion)")
			finished(app, false)

		}
	}
}


