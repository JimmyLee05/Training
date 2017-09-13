import UIKit

class MyntSimCheckTableViewCell: UITableViewCell {
	
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var stateView: UIView!

	fileprivate var isRotate = false
	fileprivate var isSuccess = false
	fileprivate var stateLayer: CALayer?

	var progress: Mynt.CheckSimProgress = .none {
		didSet {
			nameLabel.text = progress.name
		}
	}

	override func awakeFromNib() {
		super.awakeFromNib()
		selectionStyle = .none

		if stateLayer == nil {
			stateLayer = CALayer()
			stateLayer?.frame = stateView.bounds
			stateView.layer.addSublayer(stateLayer!)
		}
	}

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}

	func setState(isSuccess: Bool) {
		self.isSuccess = isSuccess
		stateLayer?.contents = isSuccess ? UIImage(named: "myntgps_check_com")?.cgImage : UIImage(named: "loading")?.cgImage
		if isSuccess {
			stopRotate()
		} else {
			startRotate()
		}
	}

	func stopRotate() {
		isRotate = false
		stateLayer?.removeAllAnimations()
	}

	func startRotate() {
		if isRotate || isSuccess { return }
		isRotate = true
		let animation = CABasicAnimation(keyPath: "transform.rotation.z")
		animation.fromValue 		= 0
		animation.toValue 			= Double.pi * 2
		animation.duration 			= 1
		animation.autoreverses 		= false
		animation.fillMode 			= kCAFillModeForwards
		animation.repeatCount 		= Float.infinity
		stateLayer?.add(animation, forKey: "rotate")
	}
}


