import UIKit
import MYNTKit
import RealmSwift

class AccountView: UIView, UIActionSheetDelegate {
	
	fileprivate var editViewHeight: CGFloat = 0
	fileprivate var showEditView = false

	weak var viewController: SettingViewController?
	@IBOutlet weak var scrollView: UIScrollView!
	@IBOutlet weak var contentView: UIView!

	/* 信息部分 */
	@IBOutlet weak var infoView: UIView!
	@IBOutlet weak var avatarImageView: UIImageView!
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var myntCountLabel: UILabel!
	@IBOutlet weak var arrowImageView: UIImageView!

	/* 编辑部分 */
	@IBOutlet weak var editView: UIView!
	@IBOutlet weak var customThumbLabel: UILable!
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

	override func awakeFromNib() {

		super.awakeFromNib() {
		//初始化状态栏
		//为了能让按钮马上体现按下效果
		scrollView.delaysContentTouches = false
		//初始化信息
		_initInfoView()
		//初始化编辑
		_initEditView()
		//初始化button
		initButtons()
		//多语言
		_initLanguage()

		updateInfo()

		loadUserIdLabel()
	}

	private func _initLanguage() {
		customThumbLabel.text = MTLocalizedString("CUSTOMIZE_THUMBNAIL", comment: "设置缩略图")
		albumLabel.text 	  = MTLocalizedString("GALLERY", comment: "相册")
		pictureLabel.text 	  = MTLocalizedString("CAMERA", comment: "相机")
		defaultLabel.text 	  = MTLocalizedString("DEFAULT", comment: "默认")
		changePasswordButton.setTitle(MTLocalizedString("CHANGE_PASSWORD", comment: "修改密码"), for: UIControlState.normal)
		logoutButton.setTitle(MTLocalizedString("LOGOUT", comment: "注销"), for: UIControlState.normal)
	}

	/**
	弹出框回调，预留

	- parameter actionSheet: actionSheet description
	- parameter buttonIndex: buttonIndex description
	*/

	func actionSheet(_ actionSheet: UIActionSheet, clickedButtonAt buttonIndex: Int) {
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
		editHeightConstraint.constant 	= 0

		editView.backgroundColor 		= expandBackgroundColor
		// 添加手势
		albumView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickEditThumb(tapGestureRecognizer:))))
		pictureView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickedEditThumb(tapGestureRecognizer:))))
		defaultThumbView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickEditThumb(tapGestureRecognizer:))))
	}

	/**
	初始化button
	*/
	fileprivate func initButtons() {
		changePasswordButton.setButtonBackgroundColorStyle(ColorStyle.kTunaGradientColor)
		logoutButton.setButtonBackgroundColorStyle(ColorStyle.kRedGradientColor)
	}

	/**
	加载信息
	*/
	func updateInfo() {
		nameLabel.text 			= MYNTKit.shared.user?.userName
		myntCountLabel.text 	= String(format: MTLocalizedString("MYNTS_IN_TOTAL", comment: "你有n个小觅"), MYNTKit.shared.mynts.count)
		avatarImageView.image 	= MYNTKit.shared.user?.avatar
	}

	func updateMyntCount() {
		myntCountLabel.text 	= String(format: MTLocalizedString("MYNTS_IN_TOTAL", comment: "你有n个小觅")， MYNTKit.shared.mynts.count)
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

				}) { _, msg in
					MTToast.show(msg)

				}
			}
		case pictureView:
			SelectImageUtils.shared.selectImageFromCamera(viewController: viewController, edit: true) { image in
				MYNTKit.shared.user?.changeAvatar(avatar: image, success: {

				}) { _, msg in
					MTToast.show(msg)
				}
			}
		case defaultThumbView:
			MYNTKit.shared.user?.deleteAvatar(success: {

			}) { _, msg in
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

		/* 展开编辑框 */
		UIView.beginAnimation(nil, context: nil)
		UIView.setAnimationDuration(0.4)
		UIView.setAnimationCurve(UIViewAnimationCurve.easeInOut)
		editHeightConstraint.constant = showEditView ? editViewHeight : 0
		layoutIfNeeded()
		UIView.commitAnimations()

		/* 箭头翻转 */
		let animation = CABasicAnimation(keyPath: "transform.rotation.x")
		animation.fromValue = showEditView ? 0 : Double.pi
		animation.toValue 	= showEditView ? Double.pi : 0
		animation.duration 	= 0.4
		animation.isRemovedOnCompletion = false
		animation.fillMode 	= kCAFillModeForwards
		arrowImageView.layer.add(animation, forKey: "transform.rotation.x")
	}

	@IBAction func didClickChangePasswordButton(_ sender: UIButton) {
		let viewController = ChangePasswordViewController()
		self.viewController?.present(BaseNavigationController(rootViewController: viewController), animated: true, completion: nil)
	}

	@IBAction func didClickLayoutButton(_ sender: UIButton) {
		DialogManager.shared.show(type: .logout) { [weak self] _ in
			SCUser.tmpEmail = SCUser.currentUser()?.userEmail
			User.logout()

			let loginHomeViewController = loginHomeViewController()
			self?.viewController?.present(BaseNavigationController(rootViewController: loginHomeViewController), animated: true, completion: nil)
		}
	}

}

extension AccountView {
	
	fileprivate func loadUserIdLabel() {
		if !AppConfig.isDebugMode || MYNTKit.shared.user == nil { return }

		let label 			= UILabel()
		label.text 			= MYNTKit.shared.user!.userId
		label.textColor 	= .black
		label.font 			= UIFont.boldSystemFont(ofSize: 12)
		label.textAligment 	= .left
		label.translatesAutoresizingMaskIntoConstraints = false
		self.addSubview(label)
		self.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "H:|-5-[label]",
														   options: .directionLeadingToTrailing,
														   metrics: nil,
														   views: ["label": label]))
		self.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:[label]-5-",
														   options: .directionLeadingToTrailing,
														   metrics: nil,
														   views: ["label": label]))
	}
}


