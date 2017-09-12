import UIKit
import MarkdownView

extension Mynt.CheckSimError {
	
	var name: String {
		switch self {
		case .mobileBluetoothError:
			return MTLocalizedString("SIM_CHECK_PHONE_TITLE", comment: "")
		case .myntDisconnected:
			return MTLocalizedString("SIM_CHECK_MYNT_TITLE", comment: "")
		case .mobileNetError:
			return MTLocalizedString("SIM_CHECK_APP_TITLE", comment: "")
		case .myntNoSim:
			return MTLocalizedString("SIM_CHECK_CARD_TITLE", comment: "")
		case .myntNetError:
			return MTLocalizedString("SIM_CHECK_NET_TITLE", comment: "")
		case .notGPS:
			return ""
		}
	}

	var message: String {
		switch self {
		case  .mobileBluetoothError:
			return "SIM_ERROR_1"
		case .myntDisconnected:
			return "SIM_ERROE_2"
		case .mobileNetError:
			return "SIM_ERROR_3"
		case .myntNoSim:
			return "SIM_ERROR_4"
		case .myntNetError:
			return "SIM_ERROR_5"
		case .notGPS:
			return ""
		}
	}
}

extension Mynt.CheckSimProgress {
	
	var name: String {
		switch self {
		case .mobileBluetooth:
			return MTLocalizedString("SIM_CHECK_PHONE_TITLE", comment: "")
		case .
		}
	}
}



















