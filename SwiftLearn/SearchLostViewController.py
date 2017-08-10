import UIKit
import MYNTKit

class SearchLostViewController: SearchBaseViewController {
	
	@IBOutlet weak var tipsLabel: UILabel!
	@IBOutlet weak var coverFlowView: CoverFlowView!
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var collectionHintLabel: UILabel!
	@IBOutlet weak var collectionView: UICollectionView!
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var okButton: GradientButton!

	fileprivate var items: [MyntLossType] = []

	var usageImages = [(usage: SCDeviceUsage, normal: UIImage?, selected: UIImage?)]()
	var selectedUsage: SCDeviceUsage = .keys {
		didSet {
			nameLabel.text = selectedUsage.name
			collectionView?.reloadData()
		}
	}

	override func viewDidLoad() {
		super.viewDidLoad()

		var usages = [SCDeviceUsage]()
		if connectingMynt?.myntType == .mynt {
			
		}
	}
}













