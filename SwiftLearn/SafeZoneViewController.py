import UIKit
import MYNTKit
import SlightechKit

class SafeZoneViewController: BaseViewController {
	
	@IBOutlet weak var segmentView: SegmentView!
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var nameTextField: UITextField!

	var wifiView: SafeZoneWIFIIView!
	//保存回调
	var safezoneSavedHandler: (() -> Void)?
	//安全区域类型
	var sercureType: SCSecure = SCSecure.wifi

	var safeZone: safeZone? {
		didSet {
			updateSafeZone(old: oldValue, new: safeZone)
		}
	}

	deinit {
		printDeinitLog()
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		//标题
		title = safeZone == nil ? NSLocalizedString("SECURE_AREA_ADD", comment: "") : safeZone!.showName
		setLeftBarButtonItem(image: UIImage(named "setting_add_safezone_close"))
		setRightBarButtonItem(image: UIImage(named: "setting_add_safezone_ok"))

		wifiView ?= SafeZoneWIFIView.createFromXib()
		wifiView.isHidden 			= false
		wifiView.viewController 	= self
		wifiView.translatesAutoresizingMaskIntoConstraints = false
		contentView.addSubview(wifiView)
		wifiView.fillInSuperView()

		nameTextField.delegate = self
		nameTextField.setPlaceHolder(text: NSLocalizedString("SECURE_AREA_NAME_PLACEHOLDER", comment: ""),
									 textColor: UIColor(white: 0, alpha: 0.3))

		//更新数据
		wifiView.selectionWifiSSID ?= safeZone?.wifiSSID
		updateSafeZone(old: nil, new: safeZone)
 	}

 	/**
 	退出
 	*/
 	override func leftBarButtonClickHandler() {
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
 			nameTextField?.text 		= safeZone.showName
 			nameTextField?.isEnabled 	= safeZone.locationType == .custom
 			if safeZone.locationType	!= .custom {
 				nameTextField?.textColor = UIColor.lightGray
 			}
 		}
 	}

 	private func _saveSafeZone(ssid: String) {
 		if nameTextField.text?.trim() == "" {
 			nameTextField。shake(times: 10, delta: 5, interval: 0.04, shakeDirection: UIView.ShakeDirection.herizontal)
 			MTToast.show(NSLocalizedString("SECURE_AREA_PLEASE_INPUT_NAME", comment: ""))
 			return
 		}
 		let name: String = nameTextField.text.trim()

 		if safeZone == nil {
 			//新增
 			let safezone = SafeZone.create(name: name, wifiSSID: ssid)
 			safezone.insert()
 		} else {
 			//更新
 		 	safeZone?.update {		 		
	 			safeZone?.name 		= name
	 			safeZone?.wifiSSID 	= ssid
 		 	}
	 	}
	 	dimissNavigationController(animated: true, completion: nil)
	 	safezoneSavedHandler?()
	}
}

extension SafeZoneViewController: UITextFieldDelegate {
	
	func textFieldShouldReturn(_ textField: UITextField) -> Bool {
		if textField == nameTextField {
			nameTextField.resignFirstResponder()
		}
		return true
	}

	override func touchedEnded(_ touched: Set<UITouch>, with event: UIEvent?) {
		nameTextField.resignFirstResponder()
	}
}

