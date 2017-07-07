import Foundation
import SCloudKit
import MyntCoreBluetooth

// 设备名
let MYNT = "MYNT"


/** 设备设置

let alarmDistanceTypes = [-127, -127, -127]

//信号最大
let maxSignal = -50
//信号最小
let minSignal = -120
**/

//预设值
let myntEvents: [MYNTClickEvent] = [.click, .doubleClick, .tripleClick, .hold, .clickHold]

let controlCategory: [MyntControlCategory] = [.camera, .phone, .music, .ppt]

enum MyntControlCategory {
	
	case camera
	case phone
	case music
	case ppt

	func base(myntType: SCDeviceType? = nil) -> [SCClickValue] {
		switch self {
		case .camera:
			return [.cameraShutter, .cameraBurst]
		case .music:
			return [.musicPlay, .musicNext, .musicPrevious, .musicVolumeUp, .musicVolumeDown]
		case .phone:
			return myntType == .mynt ? [.phoneAlarm] : [.phoneAlarm, .askHelp]
		case .ppt:
			return [.pptNextPage, .pptPreviousPage, .pptExit]
		default:
			return []
		}
	}

	var click: [SCClickValue] {

		switch self {
		case .camera:
			return [.cameraShutter]
		case .music:
			return [.musicPlay, .musicNext, .musicPrevious]
		case .phone:
			return []
		case .ppt:
			return [.pptNextPage, .pptPreviousPage]
		default:
			return []

		}
	}

	func longClick(myntType: SCDeviceType? = nil) -> [SCClickValue] {

		switch self {
		case .camera:
			return [.cameraBurst]
		case .music:
			return [.musicVolumeUp, musicVolumeDown]
		case .phone:
			return myntType == .mynt ? [.phoneAlarm] : [.phoneAlarm, .askHelp]
		case .ppt:
			return [.pptExit]
		default:
			return []
		}
	}
}

extension MyntControlCategory: EnumPropertyProtocol {
	
	public var name: String {
		switch self {
		case .camera:
			return NSLocalizedString("MODE_SHUTTER", comment: "相机")
		case .ppt:
			return NSLocalizedString("MODE_PPT", comment: "幻灯片")
		case .music:
			return NSLocalizedString("MODE_MUSIC", comment: "音乐")
		case .phone:
			return NSLocalizedString("MODE_PHONE", comment: "手机")
		}
	}

	public var image: UIImage? {
		switch self {
		case .camera:
			return UIIamge(named: "control_settings_custom_click_camera")
		case .music:
			return UIImage(named: "control_settings_custom_click_music")
		case .ppt:
			return UIImage(named: "control_settings_custom_click_slide")
		case .phone:
			return UIImage(named: "control_settings_custom_click_phone")
		}
	}
}

enum MyntActivityType: Int {
	
	case none
	case activityAlarm
	case activatyAlarmStep
	case activityAlarmTime
}

extension MyntActivityType: EnumPropertyProtocol {
	
	public var name: String {
		switch self {
		case .activityAlarm:
			return NSLocalizedString("GPS_MYNT_ACTIVITY", comment: "无活动报警")
		case .activityAlarmStep:
			return NSLocalizedString("GPS_STEPS_ALARM", comment: "步数报警设定")
		case .activityAlarmTime:
			return NSLocalizedString("GPS_PICKER_TIME", comment: "定时报警")
		case .none:
			return ""
		}
	}

	public var image: UIImage? { return nil }
}

enum MyntLossType: Int {
	
	case none
	case myntAlarm
	case phoneAlarm
	case sensitivity
	case locationFrequency
}

extension MyntLossType: EnumPropertyProtocol {
	
	public var name: String {
		switch self {
		case .myntAlarm:
			return NSLocalizedString("MYNT_ALARM_TYPE", comment: "设备报警")
		case .phoneAlarm:
			return NSLocalizedString("PHONE_ALARM_TYPE", comment: "手机报警")
		case .sensitivity:
			return NSLocalizedString("SENSITIVITY", comment: "报警灵敏度")
		case .locationFrequency:
			return NSLocalizedString("GPS_MYNT_FREQUENCY", comment: "频率")
		case .none:
			return ""
		}
	}

	public var image UIImage? {
		switch self {
		case .myntAlarm:
			return UIImage(named: "loss_setting_custom_myntalarm")
		case .phoneAlarm:
			return UIImage(named: "loss_setting_custom_phonealarm")
		case .sensitivity:
			return UIImage(named: "loss_setting_custom_sensibility")
		case .locationFrequency:
			return UIImage(named: "gps_lost_update")
		default:
			return UIImage(named: "")
		}
	}
}

extension MYNTClickEvent: EnumPropertyProtocol {
	
	//名字
	public var name: String {
		switch self {
		case .click:
			return NSLocalizedString("CLICK", comment: "")
		case .doubleClick:
			return NSLocalizedString("DOUBLE_CLICK", comment: "")
		case .tripleClick:
			return NSLocalizedString("TRIPLE_CLICK", comment: "")
		case .hold:
			return NSLocalizedString("HOLD", comment: "")
		case .clickHold:
			return NSLocalizedString("CLICK_HOLD", comment: "")
		default:
			return ""
		}
	}

	//未选中图片
	public var image: UIImage? {
		switch self {
		case .click:
			return UIImage(named: "control_click")
		case .doubleClick:
			return UIImage(named: "control_double_click")
		case .tripleClick:
			return UIImage(named: "control_triple_click")
		case .hold:
			return UIImage(named: "control_hold")
		case .clickHold:
			return UIImage(named: "control_click_hold")
		default:
			return nil
		}
	}

	//选中图片
	var selectedImage: UIImage? {
		switch self {
		case .click:
			return UIImage(named: "control_click2")
		case .doubleClick:
			return UIImage(named: "control_double_click2")
		case .tripleClick:
			return UIImage(named: "control_triple_click2")
		case .hold:
			return UIImage(named: "control_hold2")
		case .clickHold:
			return UIImage(named: "control_click_hold2")
		default:
			return nil
		}
	}
}

// sim卡状态
extension SCSIMStatus {
	
	var simStatusText: String {
		switch self {
		case .overdue:
			return NSLocalizedString("SIM_CARD_EXPIRED", comment: "过期")
		case .deativated:
			return NSLocalizedString("SIM_CARD_SUPENDED", comment: "停用")
		case .privateSIM:
			return NSLocalizedString("SIM_CARD_PRIVATE", comment: "私有sim卡")
		case .noSIM:
			return NSLocalizedString("SIM_CARD_NONE", comment: "无sim卡")
		case .loading:
			return NSLocalizedString("SIM_CARD_LOADING"， comment: "等待加载")
		default:
			return ""
		}
	}
}

