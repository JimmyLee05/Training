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

	

	}
}





















