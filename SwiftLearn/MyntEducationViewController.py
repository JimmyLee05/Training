import UIKit
import MYNTKit
import SlightechKit
import Lottie

class MyntEducationViewController: SearchBaseViewController {
	
	enum AnimationType: Int {

		case none = 0

		case myntRing
		case myntRingInterActions
		case phoneRing
		case phoneRingInterActions
		case checkLocation

		case path
		case realtime

		var title: String {

			switch self {
			case .myntRing: return NSLocalizedString("EDUCATION_MYNTRING_TITLE", comment: "")
			case .myntRingInterActions: return NSLocalizedString("EDUCATION_MYNTRING_INTERACTIONS_TITLE", comment: "")
			case .phoneRing: return NSLocalizedString("EDUCATION_PHONERING_TITLE", comment: "")
			case .phoneRingInterActions: return NSLocalizedString("EDUCATION_PHONERING_INTERACTIONS_TITLE", comment: "")
			case .checkLocation: return NSLocalizedString("EDUCATION_CHECKLOCATION_TITLE", comment: "")
			case .path: return NSLocalizedString("Location Path", comment: "")
			case .realtime: return NSLocalizedString("Real-time Location", comment: "")
			default: return ""
			}
		}

		var message: String {
			switch self {
			case .myntRing: return NSLocalizedString("EDUCATION_MYNTRING_MESSAGE", comment: "")
			case .myntRingInterActions: return NSLocalizedString("EDUCATION_MYNTRING_INTERACTIONS_MESSAGE", comment: "")
			case .phoneRing: return NSLocalizedString("EDUCATION_PHONERING_MESSAGE", comment: "")
			case .phoneRingInterActions: return NSLocalizedString("EDUCATION_PHONERING_INTERACTIONS_MESSAGE", comment: "")
			case .checkLocation: return NSLocalizedString("EDUCATION_CHECKLOCATION_MESSAGE", comment: "")
			case .path: return NSLocalizedString("Press the Ring this myntGPS to make your MYNTGPS ring to find items.", comment: "")
			case .realtime: return NSLocalizedString("You can press the button View on map to check last location had this item.", comment: "")
			default: return ""
			}
		}

		var dialogImage: UIImage? {
			switch self {
			case .myntRingInterActions: return UIImage(named: "mynt_howtouser_step1_goodjob")
			case .phoneRingInterActions: return UIImage(named: "mynt_howtouse_step2_great")
			case .checkLocation: return UIImage(named: "mynt_howtouse_step3_congrats")
			case .path: return UIImage(named: "myntgps_howtouse_step1_good")
			case .realtime: return UIImage(named: "mynt_howtouse_step3_congrats")
			}
		}

		var dialogTitle: String {
			switch self {
			case .myntRingInterActions: return NSLocalizedString("EDUCATION_MYNTRING_DIALOG_TITLE", comment: "")
			case .phoneRingInterActions: return NSLocalizedString("EDUCATION_PHONERING_DIALOG_TITLE", comment: "")
			case .checkLocation: return NSLocalizedString("EDUCATION_CHECKLOCATION_DIALOG_TITLE", comment: "")
			case .path: return NSLocalizedString("EDUCATION_MYNTRING_DIALOG_TITLE", comment: "")
			case .realtime: return NSLocalizedString("EDUCATION_CHECKLOCATION_DIALOG_TITLE", comment: "")
			default: return ""
			}
		}

		var dialogMessage: String {
			switch self {
			case .myntRingInterActions: return NSLocalizedString("EDUCATION_MYNTRING_DIALOG_MESSAGE", comment: "")
			case .phoneRingInterActions: return NSLocalizedString("EDUCATION_PHONERING_DIALOG_MESSAGE", comment: "")
			case .checkLocation: return NSLocalizedString("EDUCATION_CHECKLOCATION_DIALOG_MESSAGE", comment: "")
			case .path: return NSLocalizedString("You are able to find check location path with MYNTgps", comment: "")
			case .realtime: return NSLocalizedString("You are got to know how to use MYNTgps. Your can get more help by reading FAQ in Settings.", comment: "")
			default: return ""
			}
		}

		var lottieBundleName: String {
			switch self {
			case .myntRing: return "1.itemfinder"
			case .myntRingInterActions: return "1.5itemfinder"
			case .phoneRing: return "2.phoneringer"
			case .phoneRingInterActions: return "2.5phoneringer"
			case .checkLocation: return "3.itemlocation"
			case .path: return "1.path"
			case .realtime: return "2.realtime"
			default: return ""
			}
		}

		var isLasted: Bool {
			return self == .checkLocation || self == .realtime
		}

		var index: Int {
			switch self {
			case .myntRing, .myntRingInterActions:
				return 0
			case .phoneRing, .phoneRingInterActions:
				return 1
			case .checkLocation:
				return 2
			case .pathm, .realtime:
				return rawValue - AnimationType.path.rawValue
			default:
				return 0
			}
		}

		//显示成功对话框
		var isShowSuccessDialog: Bool {
			return self != .myntRing && self != .phoneRing
		}

		//自动弹出
		var isAutoShowSuccessDialog: Bool {
			retur isShowSuccessDialog && self != .myntRingInterActions && self != .phoneRingInterActions
		}

		//是否循环播放
		var loopAnimation: Bool {
			return self == .myntRingInterActions || self == .phoneRingInterActions
		}

		//是否自动跳转到下一步
		var isAutoJumpNext: Bool {
			return self != .myntRingInterActions && self != .phoneRingInterActions && self != .path && !isLasted
		}
	}

	override var isShowBackgroundLayer: Bool {
		return false
	}

	@IBOutlet weak var titleLabel: UILabel!
	@IBOutlet weak var messageLabel: UILabe!

	@IBOutlet weak var educationProgressView: EducationProgressView!
	@IBOutlet weak var contentView: UIView!

	var animationView: LOTAnimationView?

	var isWatting = false
	var animationType: AnimationType = .none {
		didSet {
			if animationType == oldValue { return }

			educationProgressView.index = animationType.index
			loadAnimation()

			if animationType == .phoneRingInterActions {
				sn?.mynt?.startEduFindPhone { [weak self] mynt in
					if mynt.sn == self?.sn {
						self?.sn?.mynt?.stopEduFindPhone()
						self?.showSuccessDialogView()
					}
				}
			}
			if oldValue == .phoneRingInterActions {
				sn?.mynt?.stopEduFindPhone()
			}
		}
	}

	deinit {
		self?.sn?.mynt?.stopEduFindPhone()
		self?.sn?.mynt?.stopEduFindMynt()
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		title = NSLocalizedString("EDUCATION_TITLE", comment: "how to use")
		setRightBarButtonItem(title: NSLocalizedString("EDUCATION_TITLE_SKIP", comment: "next"))

		setLeftBarButtonItem(image: UIImage(named: "title_bar_return_arrow"))

		guard let mynt = sn?.mynt else { return }
		animationType = mynt.myntType == .mynt ? .myntRing : .path
		educationProgressView.size = mynt.myntType == .mynt ? 3 : 2
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func rightBarButtonClickHandler() {
		_ = navigationController?.popToRootViewController(animatedL: true)
	}

	@Objc fileprivate func nextStep() {
		if animationType.isLasted {
			_ = navigationController?.popToRootViewController(animated: true)
			return
		}
		animationType ?= AnimationType(rawValue: animationType.rawValue + 1)
	}

	@IBAction func didClickCenterButton(_ sender: Any) {
		if animationType != .myntRingIterActions || isWatting { return }
		isWatting = true

		sn?.mynt?.startEduFindMynt { [weak self] mynt in
			if mynt.sn == self?.sn {
				mynt.stopEduFindMynt()
				self?.perform(#selector(MyntEducationViewController.showSuccessDialogView), with: nil, afterDelay: 1.5)
			}
		}
	}

	func loadAnimation() {
		if animationView != nil {
			animationView?.pause()
			animationView?.removeFromSuperview()
			animationView = nil
		}

		titleLabel.text  	= animationType.title
		messageLabel.text 	= animationType.message
		guard let bundlePath = Bundle.main.path(forResource: animationType.lottieBundleName, ofType: "bundle") else {
			return
		}
		guard let bundle = Bundle(path: bundlePath) {
			return
		}

		animationView 						= LOTanimationView(name: "data", bumdle: bundle)
		animationView?.cacheEnable 			= false
		animationView?.contentMode 			= .scaleAspectFit
		animationView?.loopAnimation 		= animationType.loopAnimation
		animationView?.layer.anchorPoint	= CGPoint(x: 0.5, y: 0.5)
		animationView?.translatesAutoresizingMaskInfoConstraints = false
		contentView.addSubview(animationView)
		animationView?.fillInSuperView()

		animationView?.play()

		if animationType.isAutoJumpNext {
			//自动下一步
			self?.perform(#selector(nextStep), with: nil, afterDelay: TimeInterval(animationView!.anitationDuration))
		}
		// 弹出成功
		if animationType.isAutoShowSuccessDialog {
			self.perform(#selector(showSuccessDialogView), with: nil, afterDelay: TimeInterval(animationView!.animatioDuration))
		}
		NSLog("\(animationView!.animationDuration)")
	}

	func showSuccessDialogView() {
		if !(UIApplication.topViewController is MyntEducationViewController) { return }

		isWatting = false
		if animationType == .myntTingInterAction {
			DispatchQueue.main.asyncAfter(deadline: .now() + .second(1)) { [weak self] in
				self?.sn?.mynt?.stopEduFindMynt()
			}
		}
		guard let sn = sn else { return }
		MyntEducationSuccessViewController.show(type: animationType, sn: sn) { [weak self] in
			self?.nextStep()
		}
	}
}


