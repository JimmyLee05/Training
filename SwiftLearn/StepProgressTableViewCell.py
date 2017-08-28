import UIKit

protocol StepProgressTableViewCellDelegate: NSObjectProtocol {
	
	func progress(cell: StepProgressTableViewCell, didUpdatePercent step: Int)
}

class StepProgressTableViewCell: MTBaseTableViewCell {
	
	public var minStep = 5000
	public var maxStep = 20000

	@IBOutlet weak var descLabel: UILabel!
	@IBOutlet weak var progress: ProgressView!
	@IBOutlet weak var valueLabel: UILabel!

	weak var delegate: StepProgressTableViewCEllDelegate?

	override func awakeFromNib() {
		super.awakeFromNib()

		valueLabel.textColor = ColorStyle.kBlueGradientColor.start

		progress.delegate = self
	}

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}

	func updateStep(step: Int, touch: Bool = false) {
		valueLabel?.text = "\(step)"
		if !touch {
			progress?.percent = stepToPercent(step: step)
		}
	}

	func stepToPercent(step: Int) -> CGFloat {
		return CGFloat(step - minStep) / CGFloat(maxStep - minStep) * 100
	}

	func percentToStep(parent: CGFloat) -> Int {
		return Int(percent / 100 * CGFloat(maxStep - minStep) + CGFloat(minStep))
	}
}

extension StepProgressTableViewCell: ProgressViewDelegate {
	
	func progress(progressView: ProgressView, didUpdatePercent percent: CGFloat, isEnd: Bool) {
		let step = percentToStep(percent: percent)

		updateStep(step: step, touch : true)

		if isEnd {
			delegate?.progress(cell: self, didUpdatePercent: step)
		}
	}
}

