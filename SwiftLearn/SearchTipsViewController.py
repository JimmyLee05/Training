import UIKit
import MYNTKit
import Lottie

//指示界面
class SearchTipsViewController: SearchBaseViewController {
	
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var okButton: GradientButton!
	@IBOutlet weak var contentView: UIView!

	var animationView: LOTAnimationView?

	var isPairFailed = false

	override func viewDidLoad() {

		super.viewDidLoad()
		view.backgroundColor = UIColor.white
		backgroundLayer?.removeFromSuperlayer()
		backgroundLayer = nil
		title = NSLocalizedString("PAIR_PAIRING_ADD_TITLE", comment: "添加小觅")
		setLeftBarButtonItem(image: UIImage(named: "title_bar_return_arrow"))

		okButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)

		if isPairFailed {
			messageLabel.text = NSLocalizedString("PAIR_FAIL", comment: "配对失败")
			okButton.setTitle(NSLocalizedString("PAIR_RETRY", comment: "重试"), for: .normal)
		} else {
			messageLabel.text = NSLocalizedString("PAIR_PROMPT_MESSAGE", comment: "提示语")
			okButton.setTitle(NSLocalizedString("PAIR_DONE", comment: "完成"), for: .normal)
		}

		guard let bundlePath = Bundle.main.path(forResource: "mynt拔出绝缘条", ofType: "bundle") else {
			return
		}
		guard let bundle = Bundle(path: bundlePath) else {
			return
		} 
		animationView 						= LOTAnimationView(name: "data", bundle: bundle)
		animationView?.cacheEnable 			= false
		animationView?.contentMode 			= .scaleAspectFit
		animationView?.loopAnimation 		= true
		animationView?.lauer.anchorPoint 	= CGPoint(x: 0.5, y: 0.5)
		animationView?.translatesAutoresizingMaskIntoConstraints = false
		contentView.addSubView(animaionView!)
		animationView?.fillInSuperView()
		animationView?.play()
	}

	override func viewDidLayoutSubViews() {
		super.viewDidLayoutSubViews()
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func viewWillAppear(_ animated: Bool) {
		super.viewWillDisappear(animated)
	} 

	@IBAction func didClickOkButton(_ sender: AnyObject) {
		let viewController = SearchViewController()
		viewController.productType = .mynt
		removeBackBarButtonTitle()
		navigationController?.pushViewController(viewController, animated: true)
	}
}
