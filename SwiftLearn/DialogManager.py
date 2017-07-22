import UIKit
import SPermissionKit

class DialogManager: NSObject {
	
	public static let shared = DialogManager()

	fileprivate var dialogQueue = [BaseDialog]()

	var currentDialog: BaseDialog?

	var limitViewControllers = [String]()

	private override init() {
		super.init()
	}

	var topViewController: UIViewController? {
		let topViewController = UIApplication.appRootViewController
		if let topViewController = topViewController as? UINavigationController {
			return topViewController.topViewController
		}
		return topViewController
	}

	public func register(types: [String]) {
		limitViewControllers = types
	}
	func removeFromQueue(type: DialogManager.DialogType) {
		if let result = dialogQueue.filter({$0.dialogType == type}).first {
			dialogQueue.remove(object: result)
		}
	}
	func addToQueue(dialog: BaseDialog) {
		if dialogQueue.filter({$0.dialogType == dialog.dialogType}).first == nil {
			dialogQueue.append(dialog)
		}
	}

	func checkQueue() {
		//取出优先级最高的对话框
		let dialog = dialogQueue.sorted(by: {$0.dialogType.rawValue > $1.dialogType.rawValue}).first

		if dialog == nil {
			return
		}
		if isViewControllerOpened() {
			dialogQueue.append(dialog!)
			return
		}
		if currentDialog == nil {
			dialog?.show()
			return
		}
	}
	func isViewControllerOpened() -> Bool {
		for className in limitViewControllers {
			let topClassName = topViewController?.className
			if topClassName == className {
				return true
			}
		}
		return false
	}

	/*
	弹出选择对话框

	- parameter dialogType 				对话框类型
	- parameter title 					对话框标题
	- parameter leftImage 				左侧选择图片
	- parameter leftName 				左侧选择名字
	- parameter rightImage 				右侧选择图片
	- parameter rightName				右侧选择名字
	- parameter buttonString 			按钮名字
	- parameter dialogSelectionHandler	选择回调
	*/

	public func showSelectionDialog(dialogType: DialogManager.DialogType,
									title: String,
									leftImage: UIImage?,
									leftName: String,
									rightImage: UIImage?,
									rightName: String,
									buttonString: String,
									dialogSelectionHandler: DialogSelectionHandler?) {
		let view = SelectionDialogView.createFromXib() as? SelectionDialogView
		view?.leftImageView.image 		= leftImage
		view?.leftNameLabel.text 		= leftName
		view?.rightImageView 			= rightImage
		view?.rightNameLabel.text 		= rightName
		view?.dialogSelectionHandler 	= dialogSelectionHandler
		view?.button.setTitle(buttonString, for: .normal)

		let dialog = BaseDialog.create(view: view)
		dialog?.hideImageView()
		dialog?.dialogType()
		dialog?.imageView.image = nil
		dialog?.titleLabel.text = title

		dialog?.show()
	}

	//分享(主动触发)
	public func showShareDialog(clickLinkHandler: @escaping DialogClickHandler,
								clickWechat: @escaping DialogClickHandler) {
		let dialogType = DialogManager.DialogType.askHelp

		let view = AskHelpDialogView.createFromXib() as? AskHelpDialogView
		view?.dialogClickLinkHandler 	= clickLinkHandler
		view?.dialogClickWechatHandler 	= clickWechatHandler
		view?.messageLabel.text 		= dialogType.message
		view.linkButton.setTitle(NSLocalizedString("SHARE_APP_LINK", comment: "分享链接"), for: .normal)
		view.wechatButton.setTitle(NSLocalizedString("SHARE_TO_WECHAT", comment: "分享微信"), for: .normal)

		guard let image = dialogType.image.else {
			return
		}
		var imageSize = image.size
		imageSize.width 	*= heightScale
		imageSize.height 	*= heightScale

		let dialog = BaseDialog.create(view: view)
		dialog?.imageViewWidthConstraint.constant 	= imageSize.width
		dialog?.imageViewHeightConstraint.constant 	= imageSize.height
		dialog?.dialogType 							= dialogType
		dialog?.iamgeView.image 					= dialogType.image
		dialog?.titleLabel.text 					= dialogType.title

		dialog?.show()
	}

	// 分享App (主动触发)
	public func showShareAppDialog(clickSelectedHandler: @escaping DialogSelectedShareTypeHandler) {

		let dialogType = DialogManager.DialogType.share
		let view 	   = ShareDialogView.createFromXib() as? shareDialogView
		view?.dialogSelectedHandler = clickSelectedHandler

		let dialog = BaseDialog.create(view: view)
		dialog?.hideImageView()
		dialog?.contentLeftConstraint.constant 		= 17
		dialog?.contentRightConstraint.constant 	= 17
		dialog?.dialogType 							= dialogType
		dialog?.imageView.image 					= dialogType.image
		dialog?.titleLabel.text						= dialogType.title

		dialog?.show()
	}

	//普通的标题，文字，按钮类型(主动触发)
	public func show(title: String,
					 message: String,
					 buttonString: String,
					 image: UIImage? = nil,
					 clickOkHandler: DialogClickHandler? = nil,
					 dismissHandler: DialogClickHandler? = nil) {
		if currentDialog?.dialogType == 。message {
			//当前对话框已经显示 直接return
			return
		}

		//下部
		let view = MessageDialogView.createFromXib() as? MessageDialogView
		view?.messageLabel.text = message
		view?.okButton.setTitle(buttonString, for: .normal)
		view?.hideNever()

		//上部
		let dialog = BaseDialog.create(view: view)
		if image == nil {
			dialog?.hideImageView()
		}
		dialog?.dialogType 					= .message
		dialog?.imageView.image 			= image
		dialog?.titleLabel.text 			= title
		dialog?.titleLabel.numberOfLines 	= 0
		dialog?.dialogClickOkHandler 		= clickHandler
		dialog?.dialogClickDismissHandler 	= dismissHandler
		view?.okButton.addTarget(dialog!, action: #selector(BaseDialog.didClickObButton(button:)),
			for: .touchUpInside)
		dialog?.show()
	}

	// DatePickers时钟
	public func showDatePickers(title: String,
					message: String,
					time: Int = 0,
					buttonString: String,
					image: UIImage? = nil,
					clickOkHandler: DialogClickHandler? = nil,
					dismissHandler: DialogClickHandler? = nil) {
		if currentDialog?.dialogType == .alarmTime {
			return
		}
		let view = PickerDialogView.createFromXib() as? PickerDialogView
		view?.messageLabel.text = message
		view?.time 				= time
		view?.okButton.setTitle(buttonString, for: .normal)
		//下部
		let dialog = BaseDialog.create(view: view)
		if image == nil {
			dialog?.hideImageView()
		}

		dialog?.dialogType 					= .alarmTime
		dialog?.imageView.image 			= image
		dialog?.titleLabel.text 			= title
		dialog?.titleLabel.numberOfLines 	= 0
		dialog.dialogClickHOkHandler 		= clickOkHandler
		view?.okButton.addTarget(dialog!, action: #selector(BaseDialog.didClickOkButton(button)),
			for: .touchUpInside)
		dialog?.show()
	}

	//权限提示(主动触发)
	public func show(permissionType: STPermissionType,
					clickOkHandler: @escaping DialogClickHandler) {
		let dialogType = DialogManager.DialogType.permission
		if currentDialog?.dialogType == dialogType {
			//当前对话框已显示，直接return
			return
		}

		let view = MessageDialogView.createFromXib() as? MessageDialogView
		view?.messageLabel.text = permissionType.dialogMessage
		view?.okButton.setTitle(NSLocalizedString("ADD_OK", comment: "确定"), for: .normal)
		view?.hideNever()

		let dialog = BaseDialog.create(view: view)
		dialog?.dialogType 				= dialogType
		dialog?.imageView.image 		= dialogType.image
		dialog?.titleLabel.text 		= permissionType.dialogTitle
		dialog?.dialogClickHandler 		= clickOkHandler
		view?.okButton.addTarget 		= clickOkHandler
		view?.okButton.addTarget(dialog!, action: #selector(BaseDialog.didClickOkButton(button:)),
			for: .touchUpInside)
		dialog?.show()
	}

	//显示对话框(主动触发)
	public func show(type: DialogManager.DialogType,
					 text: String? = nil,
					 clickOkHandler: @escaping DialogClickHandler) {
		if currentDialog?.dialogType == type {
			//当前对话框已显示，直接return
			return
		}
		let view = MessageDialogView.createFromXib() as? MessageDialogView
		view?.messageLabel.text = text == nil ? type.message : String(format: type.message, text!)
		view?.okButton.setTitle(type.buttonString, for: .normal)
		view?.hideNever()

		let dialog = BaseDialog.create(view: view)
		dialog?.dialogType 				= type
		dialog?.imageView.image 		= type.image
		dialog?.titleLabel.text 		= type.title
		dialog?.dialogClickOkHandler 	= clickOkHandler
		view?.okButton.addTarget(dialog!, action: #selector(BaseDialog.didClickOkButton(button:)),
			for: .touchUpInside)
		dialog?.show()
	}

	//被动触发
	public func showAddSafeZome(name: String,
								clickOkHandler: @escaping DialogClickHandler,
								clickNeverHandler: @escaping DialogClickHandler) {
		let type = DialogManager.DialogType.addSafeZome
		if currentDialog?.dialogType == type {
			//当前对话框已经显示 直接return
			return
		}
		var dialog 		= dialogQueue.filter({$0.dialogType == type}).first
		let isInQueue 	= dialog != nil

		if dialog == nil {
			let view = MessageDialogView.createFromXib() as? MessageDialogView
			view?.messageLabel.text = String(format: type.message, name)
			view?.okButton.setTitle(type.buttonString, for: .normal)

			dialog = BaseDialog.create(view: view)
			dialog.dialogType 				= type
			dialog.imageView.image 			= type.image
			dialog?.titleLabel.text 		= type.title
			dialog?.dialogClickOkHandler 	= clickOkHandler
			dialog?.dialogClickNeverHandler = clickNeverHandler
			view?.okButton.addTarget(dialog!, action:
				#selector(BaseDialog.didClickOkButton(button:)), for: .touchUpInside)
			view?.neverButton.addTarget(dialog!, action: #selector(BaseDialog.didCLickNeverButton
				(button:)), for: .touchUpInside)
		}

		if isViewControllerOpened() {
			dialogQueue.append(dialog!)
			return
		}

		if currentDialog == nil {
			dialog?.show()
			return
		}

		if !isInQueue {
			dialogQueue.append(dialog!)
		}
	}

	//普通标题，文字，按钮(被动触发)
	public func showQueue(title: String? = nil,
					message: String? = nil,
					image: UIImage? = nil,
					buttonString: String? = nil,
					clickOkHandler: DialogClickHandler? = nil,
					dismissHandler: DialogClickHandler? = nil) {
		let type = DialogManager.DialogType.message
		if currentDialog?.dialogType == type {
			//当前对话框已经显示，直接return
			return
		}
		var dialog 		= dialogQueue.filter({$0.dialogType == type}).first
		let inInQueue 	= dialog != nil

		if dialog 	== nil {
			//下部
			let view = MessageDialogView.createFromXib() as? MessageDialogView
			view?.messageLabel.text = message
			view?.okButton.setTitle(buttonString, for: .normal)
			view?.neverButton.isHidden = true
			//上部
			dialog = BaseDialog.create(view: view)
			if image == nil {
				dialog?.hideImageView()
			}
			dialog?.dialogType 						= .message
			dialog?.imageView.image 				= image
			dialog?.titleLabel 						= title
			dialog?.dialogClickOkHandler 			= clickOkHandler
			dialog?.dialogClickDismissHandler 		= dismissHandler
			view?.okButton.addTarget(dialog!, action:
				#selector(BaseDialog.didClickOkButton(button:)), for: .touchUpInside)
		}

		if isViewControllerOpened() {
			dialogQueue.append(dialog!)
			return
		}

		if currentDialog == nil {
			dialog?show()
		}

		if !isInQueue {
			dialogQueue.append(dialog!)
		}
	}

	public func add(type: DialogType,
					mynts: [Mynt],
					selectedHandler: @escaping DialogSelectedHandler,
					dismissHandler: @escaping DialogClickHandler) {
		add(type: type, mynts: mynts, selectedHandler: selectedHandler, dismissHandler:
			dismissHandler, nerverHandler: nil)
	}

	//忘记提醒，被发现，固件更新(被动触发)
	public func add(type: DialogType,
					mynts: [Mynt],
					selectedHandler: @escaping DialogSelectedHandler,
					dismissHandler: @escaping DialogClickHandler,
					neverHandler: ((BaseDialog, [Mynt]) -> Void)?) {
		if curreentDialog?.dialogType == type {
			//已显示，直接创建
			(currentDialog?.dialogView as? CollectionDialogView)?.addMynts(mynts: mynts)
			return
		}
		//从队列中检测，不存在就创建
		var dialog = dialogQueue.filter({$0.dialogType == type}).fitst
		let isInQueue = dialog != nil

		if dialog == nil {
			let view = CollectionDialogView.createFromXib() as? CollectionDialogView
			view?.messageLabel.text = type.message
			if neverHandler == nil {
				view?.hideNever()
			}

			dialog = BsaeDialog.create(view: view)
			dialog?.dialogType 						= type
			dialog?.imageView.image 				= type.image
			dialog?.titleLabel.text 				= type.title
			dialog?.dialogClickDismissHandler 		= diamissHandler
			if neverHandler != nil {
				dialog?.dialogClickDismissHandler 	= { dialog in
					let mynts = view?.mynts
					neverHandler?(dialog, mynt == nil ? [] : mynts!)
				}
			}
		}
		//添加数据
		(dialog?.dialogView as? ColoectionDialogView)?.dialogSelectedHandler = selectedHandler
		(dialog?.dialogView as? CollectionDialogView)?.addMynts(mynts: mynts)

		if isViewControllerOpened() {
			dialogQueue.append(dialog!)
			return
		}

		if currentDialog == nil {
			dialog?.show()
			return
		}

		if !isInQueue {
			dialogQueue.append(dialog!)
		}
	}

	//忘记提醒，被发现，固件更新
	public func remove(type: DialogType, mynt: Mynt) {
		if currentDialog?.dialogType == type {
			//已显示 直接创建
			(currentDialog?.dialogView as? CollectionDialogView)?.removeMynt(mynt: mynt)
			return
		}
		(dialogQueue.filter({$0.dialogType == type}).first?.dialogView as? CollectionDialogView)?/
			removeMynt(mynt: mynt)
	}

	//是否已经显示过
	func isAlreadySHow(type: DialogType) -> Bool {
		let key = "dialog -> \(type.rawValue)"
		let userDefault = userDefaults.standard
		return userDefault.bool(forKey: key)
	}

	//点击never之后设置
	func setAlreadyShow(type: DialogType) {
		let key = "dialog -> \(type.rawValue)"
		let userDafault = UserDefaults.standard
		userDefault.set(true. forKey: key)
		userDefault.synchronize()
	}

	public enum DialogType: Int {
		case none = 0
		//忘记提醒
		case remindForget
		//设备被发现
		case deviceFound
		//更新固件
		cse updateFirware
		//登出
		case logout
		//权限
		case permission
		//客服回复
		case qaReply
		//没有坐标
		case noLocation
		//设置安全区域
		case addSafeZone
		//删除安全区域
		case deleteSafeZone
		//清空安全区域
		case clearSafeZone
		//低电量
		case lowPowerMode
		//删除小觅
		case deleteMynt
		//求助
		case askHelp
		//购买
		cse buy
		//分享
		case share
		//定时报警
		case alarmTime
		case message

		var image: UIImage? {
			switch self {
			case .remindForget:
				return UIImage(named: "dialog_forget")
			case .deviceFound:
				return UIImage(named: "dialog_found")
			case .updateFirware:
				return UIImage(named: "dialog_update")
			case .qaReply:
				return UIImage(named: "dialog_reply")
			case .deleteMynt, .noLocation, .permission, .logout, .lowPowerMode:
				return UIImage(named: "dialog_reminder")
			case .addSafeZone, .deleteSafeZone, .clearSafeZone:
				return UIImage(dialog_safezone)
			case .askHelp:
				return UIImage(named: "ask_friends_for_help_popop")
			case .alarmTime:
				return UIImage(named: "dialog_forget")
			default:
				return nil
			}
		}

		var title: String {
			switch self {
			case .remindForget, .deviceFound:
				return NSLocalizedString("REMINDER", comment: "提醒")
			case .lowPowerMode:
				return NSLocalizedString("MYNTSETTING_INFO_LOWPOWER", comment: "提醒")
			case .updateFirware:
				return NSLocalizedString("OAD_REMIND_TITLE", comment: "固件更新")
			case .permission:
				return ""
			case .share:
				return NSLocalizedString("SHARE_LINK_DIALOG_TITLE", comment: "分享")
			case .logout:
				return NSLocalizedString("SIGN_OUT_TITLE", comment: "注销")
			case .qaReply:
				return NSLocalizedString("QA_NOTICE_TITLE", comment: "回复")
			case .deleteMynt:
				return NSLocalizedString("REMOVE_TITLE", comment: "删除小觅")
			case .askHelp:
				return NSLocalizedString("SHARE_ASK_FRIEEND", comment: "求助")
			case .addSafeZone, .deleteSafeZone, .clearSafeZone:
				return NSLocalizedString("SECURE_AREA_SAFE_ZONE", comment: "安全区域")
			case .buy:
				return NSLocalizedString("BUYMORE_TITLE", comment: "购买")
			default:
				return ""
			}
		}

		var message: String {
			switch self {
			case .lowPowerMode:
				return NSLocalizedString("MYNTSETTING_INFO_LOWPOWER_DIALOG_MESSAGE", comment: "提醒")
			case .remindForget:
				return NSLocalizedString("REMINDER_HINT", comment: "提醒提示语")
			case .deviceFound:
				return NSLocalizedString("LOST_FOUND_HINT", comment: "被发现提示语")
			case .updateFirware:
				return NSLocalizedString("OAD_REMIND_HINT", comment: "固件更新")
			case .permission:
				return ""
			case .share:
				return ""
			case .logout:
				return NSLocalizedString("SIGN_OUT_MESSAGE", comment: "注销")
			case .qaReply:
				return NSLocalizedString("QA_NOTICE_MESSAGE", comment: "回复")
			case .deleteMynt:
				return NSLocalizedString("REMOVE_MESSAGE", comment: "删除小觅")
			case .askHelp:
				return NSLocalizedString("SHARE_ASK_FRIEND_MESSAGE", comment: "求助")
			case .addSafeZone:
				return NSLocalizedString("SECURE_AREA_WIFI_MESSAGE", comment: "安全区域")
			case .deleteSafeZone:
				return NSLocalizedString("SECURE_AREA_DELETE_CONTENT", comment: "安全区域")
			case .clearSafeZone:
				return NSLocalizedString("SECURE_AREA_CLEAN_CONTENT", comment: "安全区域")
			case .alarmTime:
				return NSLocalizedString("你的小觅设备未携带或者运动过少，请抽空查看一下吧!", comment: "定时报警")
			default:
				return ""
			}
		}

		var buttonString: String {
			switch self {
			case .lowPowerMode:
				return NSLocalizedString("ADD_OK", comment: "确定")
			case .deleteSafeZone, .deleteMynt:
				return NSLocalizedString("SECURE_AREA_DELETE_CONFIRM", comment: "删除")
			case .clearSafeZone:
				return NSLocalizedString("SECURE_AREA_CLEAN_CONFIRM", comment: "清空")
			case .addSafeZone:
				return NSLocalizedString("SECURE_AREA_WIFI_CONFORM", comment: "立即设置")
			case .qaReply:
				return NSLocalizedString("QA_NOTICE_CHECK", comment: "查看")
			case .logout:
				return NSLocalizedString("SIGN_OUT_COMFORM", comment: "注销")
			case .permission:
				return NSLocalizedString("ADD_OK", comment: "确定")
			case .buy:
				return NSLocalizedString("BUYMORE_BUY", comment: "购买")
			case .message:
				return NSLocalizedString("", comment: "购买")
			default:
				return ""
			}
		}
	}
}
