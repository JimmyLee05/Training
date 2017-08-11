import UIKit

class MyntEducationSuccessViewController: SearchBaseViewController {
	
	class func show(type: MyntEducationViewController.AnimationType, sn: String, dismissHandler: (() -> Void)?) {
			let viewController = MyntEducationSuccessViewController()
			viewController.dismissHandler 	= dismissHandler
			viewController.animationType 	= type
			viewController.sn 				= sn
			viewController.modalPresentationStyle = .custom
			viewController.modalTransitionStyle   = .crossDisolve

			let animation = CATransition()
			animation.duration = 0.5
			animation.type 	   = kCATransitionPush
			animation.subtype  = kCATransitionFade
			animation.timingFunction = CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseIn)
			viewController.view.layer.add(animation, forKey: "swirchToView")

			UIApplication.topViewController?.present(viewController, animated: true, completion: nil)
		}
	override var isShowBackgroundLayer: Bool { return false }

	@IBOutlet weak var contentView: UIView!

	@IBOutlet weak var hintImageView: UIImageView!

	@IBOutlet weak var messageLabel: UILabel!

	@IBOutlet weak var titleLabel: UILabel!

	@IBOutlet weak var startButton: UIButton!

	fileprivate var gradientLayer: CAGradientLayer?

	var dismissHandler: (() -> Void)?

	var animationType: MyntEducationViewController.AnimationType = .none

	override func viewDidLoad() {

		super.viewDidLoad()
		self.view.backgroundColor = UIColor(white: 0, alpha: 0.6)

		contentView.layer.cornerRadius = 8
		startButton.layer.cornerRadius = startButton.bounds.height / 2

		//添加渐变色
		gradientLayer = CAGradientLayer()
		gradientLayer?.colors = [UIColor(red:0.29, green:0.65, blue:0.87, alpha:1.00).cgColor,
								 UIColor(red:0.39, green:0.82, blue:0.85, alpha:1.00).cgColor]

		self.view.layer.addSublayer(gradientLayer!)

		startButton.isHidden = !animationType.isLasted

		titleLabel.text = animationType.dialogTitle
		messageLabel.text = animationType.dialogMessage
		hintImageView.image = animationType.dialogImage

		startButton.setTitle(NSLocalizedString("EDUCATION_CHECKLOCATION_DIALOG_BUTTON", comment: ""), for: .normal)

		if animationType.isLasted {
			startButton.addTarget(self, action: #selector(close), for: .touchInside)
		} else {
			perform(#selector(close), width: nil, afterDelay: 3)
		}

		self.view.isUserInteractionEnabled = trye
		self.view.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(close)))
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func viewDidLayoutSubviews() {
		super.viewDidLayoutSubviews()
		gradientLayer?.frame = titleLabel.frame
		gradientLayer?.mask  = titleLabel.layer
		if gradientLayer != nil {
			titleLabel.frame = gradientLayer!.bounds
		}
	}

	@objc func close() {
		dismiss(amimated: true)
		self?.dismissHandler?()
		self?.dismissHandler = nil
	}
}



