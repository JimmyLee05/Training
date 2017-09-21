import UIKit
import MYNTKit
import SlightechKit

class SafeZoneViewController: BaseViewController {
	
	@IBOutlet weak var segmentView: SegmentView!
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var nameTextField: UITextField!

	var wifiView: SafeZoneWIFIView!
	//安全区域类型
	var sercureType: SCSecure = SCSecure.wifi

	var safeZone: SafeZone? {
		didSet {
			updateSafeZone(old: oldValue, new: safeZone)
		}
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		//标题
		title = safeZone == nil ? MTLocalizedString("SECURE_AREA_ADD", comment: ""): safeZone!.showName
		setLeftBarButtonItem(image: Resource.Image.Navigation.close)
		setRightBarButtonItem(image: UIImage(named: "setting_add_safezone_ok"))

		wifiView ?= SafeZoneWIFIView.createFromXib()
		wifiView.isHidden 			= false
		wifiView.viewController 	= self
		wifiView.translatesAutoresizingMaskIntoConstraints = false
		contentView.addSubview(wifiview)
		wifiView.fillInSuperView()

		nameTextField.delegate 		= self
		nameTextField.setPlaceholder(text: MTLocalizedString("SECURE_AREA_NAME_PLACEHOLDER", comment: ""),
									 textColor: UIColor(white: 0, alpha: 0.3))
		// 更新数据
		wifiView.selectionWifiSSID ?= safeZone?.wifiSSID
		updateSafeZone(old: nil, new: safeZone)
	}

	/**
	退出
	*/
	override func leftBarButtonClickedHandler() {
		dismissNavigationController(animated: true, completion: nil)
	}

	/**
	保存数据
	*/
	override func rightBarButtonClickedHandler() {
		if let SSID = wifiView.selectionWifiSSID, SSID != "" {
			_saveSafeZone(ssid: SSID)
		}
	}

	func updateSafeZone(old: SafeZone?, new: SafeZone?) {
		if let safeZone = safeZone {
			nameTextField?.text 			= safeZone.showName
			nameTextField?.isEndbled 		= safeZone.locationType == .custom
			if safeZone.locationType != .custom {
				nameTextField?.textColor = UIColor.lightGray
			} 
		}
	}

	
}
























