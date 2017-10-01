import UIKit
import MYNTKit
import SlightechKit
import RealmSwift

public enum PayType: Int {
	
	case wechatPay
	case aliPay
	case none

	var image: UIImage? {
		switch self {
		case .wechatPay:
			return UIImage(named: "app_settings_payment_wechat")
		case .aliPay:
			return UIImage(named: "app_setting_payment_alipay")
		case .none:
			return UIImage(named: "")
		}
	}

	
}