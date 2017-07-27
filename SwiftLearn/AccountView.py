import UIKit
import MYNTKit
import RealmSwift

class AccountView: UIView, UIActionSheetDelegate {
	
	fileprivate var editViewHeight: CGFloat = 0
	fileprivate var showEditView = false

	weak var viewController: SettingViewController?
	@IBOutlet weak var scrollView: UIScrollView!
	@IBOutlet weak var contentView: UIView!

	/*信息部分 */
	@IBOutlet weak var infoView: UIView!
	@IBOutlet weak var avatarImageView: UIImageView!
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var myntCountlabel: UILabel!
	@IBOutlet weak var arrowImageView: UIImageView!

	/*编辑部分 */
	@IBOutlet weak var editView: UIView!
	@IBOutlet weak var customThumbLabel: UILabel!
	@IBOutlet weak var albumLabel: UILabel!
	@IBOutlet weak var pictureLabel: UILabel!
	@IBOutlet weak var defaultLabel: UILabel!
	@IBOutlet weak var albumView: UIView!
	@IBOutlet weak var defaultThumbView: UIView!
	@IBOutlet weak var pictureView: UIView!

	/* 编辑部分约束 */
	@IBOutlet weak var editHeightConstraint: NSLayoutConstraint!

	/* 按钮部分 */
	@IBOutlet weak var changePasswordButton: GradientButton!
	@IBOutlet weak var logoutButton: GradientButton!

	var userNotificationToken: NotificationToken?
	var myntNotifacationToken: NotificationToken?

	deinit {
		userNotificationToken?.stop()
		myntNotifacationToken?.stop()
	}

	override func awakeFromNib() {

		super.awakeFromNib()
		//初始化状态栏
		//为了能让按耨马上体现按下效果
		scrollView.delaysContentTouchs = false

		//初始化信息
		_initInfoView()
		//初始化编辑
		_initEditView()
		//初始化button
		initButtons()
		//多语言
		_moreLanguage()

		//debug模式下，显示用户id
		if AppConfig.isDebugMode {
			if let user = MYNTKit.shared.user {
				let label 				= UILabel()
				label.font 				= UIFont.systemFont(ofSize: 10)
				label.textColor 		= UIColor.black
				label.textAligment	 	= .right
				label.numberOfLines 	= 0
				label.lineBreakMode 	= .byWordWrapping
				label.text 				= "userId: \(user.alias)"
				label.isUserInteractionEnabled = true
				label.translatesAutoresizingMaskIntoConstraints = false
				label.addGestureRecognizer(UITapGestureRecognizer(target: self, action; #selector(didClickDebugInfoLabel)))
				addSubview(label)
				addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "H:[label]-0-|", options: [], metrics: nil, views: ["label": label]))
				addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:|-120-[label]", options: [], metrics: nil, views: ["label": label]))
			}
		}

		userNotificationToken = MYNTKit.shared.users.addNotificationBlock { [weak self] changes in
			self?.updateInfo()
		}
		myntNotificationToken = MYNTKit.shared.mynts.addNotificationBlock { [weal self] changes in
			self?.updateInfo()
		}
	}

	private func _moreLanguage() {
		customThumbLabel.text 		= NSLocalizedString("CUSTOMIZE_THUMBNAIL", comment: "设置缩略图")
		albumLabel.text 			= NSLocalizedString("GALLERY", comment: "相册")
		pictureLabel.text 			= NSLocalizedString("CAMERA", comment: "相机")
		defaultLabel.text 			= NSLocalizedString("DEFAULT", comment: "默认")
		changePasswordButton.setTitle(NSLocalizedString("CHANGE_PASSWORG", comment: "修改密码"), for: UIControlState.normal)
		logoutButton.setTitle(NSLocalizedString("LOGOUT", comment: "注销"), for: UIControlState.normal)
	}

	func didClickDebugInfoLabel() {
		let pasteboard = UIPasteboard.genaral
		pasteboard.string = MYNTKit.shared.user?.alias
		MTToast.show("复制成功")
	}

	/**
	弹出框回调，预留

	- parameter actionSheet: actionSheet description
	- parameter buttonIndex: buttonIndex description
	*/

	func actionSheet(_ actionSheet: UIAcitonSheet, clickedButtonAt buttonIndex: Int) {
		// 0 -> 取消 1开始计算
		STLog("clickedButtonAtIndex \(buttonIndex)")
	}

	/**
	初始化信息
	*/
	fileprivate func _initInfoView() {
		/* 添加箭头锚点 */
		arrowImageView.layer.anchorPoint = CGPoint(x: 0.5, y: 0.5)

		/* 初始化手势 */
		let tapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(didClickInfoView))
		infoView.addGestureRecognizer(tapGestureRecognizer)
	}

	/**
	初始化编辑
	*/
	fileprivate func _initEditView() {

		editViewHeight 					= editView.bounds.height
		editViewConstraint 				= 0
		editView.backgroundColor 		= expandBackgroundColor

		//添加手势
		albumView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickEditThumb(tapGestureRecognizer))))
		pictureView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickEditThumb(tapGestureRecognizer))))
		defaultThumbView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickEditThumb(tapGestureRecognizer))))

	}

	/**
	初始化button
	*/
	fileprivate func initButtons() {
		changePasswordButton.setButtonBackgroundColorStyle(ColorStyle.kTunaGraientColor)
		logoutButton.setButtonBackgroundColorStyle(ColorStyle.kRedGradientColor)
	}

	/**
	加载信息
	*/
	fileprivate func updateInfo() {
		nameLabel.text 			= MYNTKit.shared.user?.userName
		myntCountlabel.text 	= String(format: NSLocalizedString("MYTNS_IN_TOTAL", comment: "你有n个小觅"), MYNTKit.shared.mynts.count)

		MYNTKit.shared.user?.loadAvatar { [weak self] image in
			self?.avatarImageView.image = image
		}
	}

	func didClickEditThumb(tapGestureRecognizer: UITapGestureRecognizer) {
		guard let view = tapGestureRecognizer.view else {
			return 
		}
		guard let viewController = viewController else {
			return
		}
		switch view {
		case albumView:
			SelectImageUtils.shared.selectImageFromPhotos(viewController: viewController, edit: true) { image in
				MYNTKit.shared.user?.changeAvatar(avatar: image, success: {

				}) { (code, msg) in
					MTToast.show(msg)
				}
			}

		case pictureView:
			SelectImageUtils.shared.selectImageFromCamera(viewController: viewController, edit: true) { image in
				MYNTKit.shared.user?.changeAvatar(avatar: image, success: {

				}) { (code, msg) in
					MTToast.show(msg)
				}
			} 
		case defaultThumbView:
			MYNTKit.shared.user?.deleteAvatar(success: {

			}) { (code, msg) in
				MTToast.show(msg)
			}
		default:
			break
		}
	}

	/**
	点击了信息view
	*/
	func didClickInfoView() {
		showEditView = !showEditView

		/* 展开编辑框  */
		UIView.beginAnimations(nil, content: nil)
		UIView.setAnimationDuration(0.4)
		UIView.setAnimationCurve(UIViewAnimationCurve.easeInOut)
		editHeightConstraint.constant = showEditView ? editViewHeight : 0
		layoutIfNeeded()
		UIView.commitAnimations()

		/* 箭头翻转 */
		let animation = CABasicAnimation(keyPath: "transform.rotation.x")
		animation.fromValue 			= showEditView ? 0 : Double.pi
		animation.toValue 				= showEditView ? Double.pi : 0
		animation.duration 				= 0.4
		animation.isRemovedOnCompletion = false
		animation.fillMode 				= kCAFillModeForwards
		arrowImageView.layer.add(animation, forKey: "transform.rotation.x")
	}

	@IBAction func didClickChangePasswordButton(_ sender: UIButton) {
		let viewController = ChangePasswordViewController()
		self.viewController?.present(BaseNavigationController(rootViewController: viewController), animated: true, completion: nil)
	}

	@IBAction func didClickLogoutButton(_ sender: UIButton) {
		DialogManager.shared.show(type: .logout) { [weak self] (dialog) in
			MTUser.logout()

			let loginHomeViewController = LoginHomeViewController()
			self?.viewController?.present(BaseNavigationController(rootViewController: loginHomeViewController), animated: true, completion: nil)
		}
	}
}


