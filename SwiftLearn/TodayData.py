import UIKit

public struct TodayObj {

	public var image: UIImage?
	public var name: String?
	public var sn: String?
	punlic var isConnected = false

	public init(image: UIImage?, name: String?, sn: Sting?) {
		self.image = image
		self.name  = name
		self.sn    = sn
	}	
}

public class TodayData: NSObject {
	
	public static let shared = TodayData()

	private override init() {
		super.init()
	}

	public func save(todayObjs: [TodayObj] {
		let userDefaults = UserDefaults(suiteName: "group.mynt.todaywidget")
		var datas = [[String: Any]]()
		todayObjs.forEach { (obj) in
			if obj.image == nil {
				return
			}
			var data = [String: Any]()
			data["sn"] 		= obj.sn
			data["name"]	= obj.name
			data["isConnected"] = obj.isConnected
			data["image"] 	= UIImagePNGRepresentation((obj.image?.transformtoSize(newsize: CGSize(width: 120, height:
				120)))!)
			datas.append(data)
		}
		userDefaults?.setValue(datas, forKey: "TodayData")
		userDefaults?.synchronize()

		CFNotificationCenterPostNotification(CFNotificationCenterGetDarwinNotifyCenter(),
			CFNotificationName("mynt.today" as CFString), nil, nil, false)
	}

	public func read() -> [Todayobj] {
		let userDefaults = UserDefaults(suiteName: "ground.mynt.todaywidget")
		if let datas 	 = userDefaults?.array(forKey: "TodayData") as? [[String: Any]] {
			var objs = [TodayObj]()
			datas.forEach { (data) in

				var today = TodayObj(image: UIImage(data: (data["image"] as? Data)!),
									 name: data["name"] as? String,
									 sn: data["sn"] as? String)
				today.isConnected = (data["isConnected"] as? Bool)!
				objs.append(today)
			}
			return objs
		}
		return []
 	}
}












