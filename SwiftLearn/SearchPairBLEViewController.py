import UIKit
import MYNTKit

class SearchPairBLEViewController: SearchBaseViewController {
	
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var arrowImageView: UIImageView!
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var okButton: UIButton!

	var isNew = true

	override func viewDidLoad() {
		super.viewDidLoad()
		view.backgroundColor = UIColor.white
		backgroundLayer?.removeFromSuperlayer()
		backgroundLayer = nil

		if isNew {
			setLeftBarButtonItem(image: UIImage(named: "title_bar_return_arrow"))
		} else {
			setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))
		}
		okButton.setTitle(NSLocalizedString("ADD_OK", comment: "ok"), for: UIControlState.normal)
		messageLabel.text = NSLocalizedString("PAIR_PAIRING_SUBTITLE", comment: "")
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func leftBarButtonClickHandler() {
		if isNew {
			_ = navigationController?.popToRootViewController(animated: true)
			connectingMynt?.disconnect()
		} else {
			connectingMynt?.disconnect()
			dismissNavigationController(animated: true, completion: nil)
		}
	}

	override func viewWillAppear(_ animated: Bool) {
		super.viewWillAppear(animated)

		let animated = CABasicAnimation(keyPath: "position")
		animation.byValue = NSValue(cgPoint: CGPoint(x: 15, y: -8))
		animation.repeatCount = Float.infinity
		animation.duration = 1
		arrowImageView.layer.add(animation, forKey: "arrow-move")
	}

	override func viewWillDisappear(_ animated: Bool) {
		super.viewWillDisappear(animated)
		arrowImageView.layer.removeAllAnimations()
	}
}

