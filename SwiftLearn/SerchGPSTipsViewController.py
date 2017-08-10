import UIKit
import MYNTKit
import Lottie

//指示界面
class SearchGPSTipsViewController: SearchBaseViewController {
	
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var okButton: GradientButton!
	@IBOutlet weak var contentView: UIView!

	var animatedView: LOTAnimationView?

	var isPairFailed: Bool = false

	override func viewDidLoad() {

		super.viewDidLoad()
		view.backgroundColor = UIColor.white
		backgroundLayer?.removeFromSuperlayer()
		backgroundLayer = nil
		title = NSLocalizedString("PAIR_PAIRING_ADD_TITLE", comment: "添加小觅")
		setLeftBarButtonItem(image: UIImage(named: "title_bar_return_arrow"))

		okButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		okButton.layer.cornerRadius = okButton.bounds.height / 2
		okButton.setTitle(NSLocalizedString("ADD_OK", comment: "添加小觅"), for: .normal)
		messageLabel.numberOfLines  = 0
		messageLabel.text 			= NSLocalizedString("PAIR_PROMPT_GPS_MESSAGE", comment: "添加小觅")

		guard let bundlePath 		= Bundle.main.path(forResource: "gps长按开机", ofType: "bundle") else {
			return
		}
		guard let bundle = Bundle(path: bundlePath) else {
			return
		}

		animationView 												= LOTAnimationView(name: "data", bundle: bundle)
		animationView?.cacheEnable 									= false
		animationView?.contentMode 									= .scaleAspectFit
		animationView?.loopAnimation	 							= true
		animationView?.layer.anchorPoint 							= CGPoint(x: 0.5, y: 0.5)
		animationView?.translatesAntoresizingMaskIntoConstraints 	= false
		animationView.addSubview(animationView!)
		animationView?.fillInSuperView()
		animationView?.play()
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func viewWillAppear(_ animated: Bool) {
		super.viewWillAppear(animated)
	}

	override func viewWillDisappear(_ animated: Bool) {
		super.viewWillDisappear(animated)
	}

	@IBAction func didClickOKButton(_ sender: Any) {
		let viewController = SearchViewController()
		viewController.productType = .myntGPS
		removeBackBarButtonTitle()
		navigationController?.pushViewController(viewController, animated: true)
	}

}

