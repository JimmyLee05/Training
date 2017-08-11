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
			items = [.phoneAlarm, .myntAlarm, .sensitivity]
			usage = [.keys, wallet, .purse, .wallet, .purse, .car, .child, .pet, .backpack, .suitcase, .luggagecase]
		}

		usage.forEach { [usage] in
			let normal = UIImage.create(with: 50, icon: usage.image)
			let selected = UIImage.create(with: 50, icon: usage.image, color: usage.usageColor)
			uasgeImages.append((usage: usage, normal: normal, selected: selected))
		}
		selectedUsage = usageImages[0].usage

		selfLeftBarButtonItem(image: UIImage(named: "title_bar_return_arrow"))

		coverFlowView.delegate 		= self
		coverFlowView.dataSource 	= self

		collectionView.register(with: MyntConfigCollectionCell.self)
		collectionView.delegate 	= self
		collectionView.dataSource 	= self

		okButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		_moreLanguage()
	}

	private func _moreLanguage() {
		title = NSLocalizedString("PAIR_PAIRING_ADD_TITLE", comment: "添加小觅")
		tipsLabel.text = NSLocalizedString("ADD_MYNT_TIPS", comment: "提示语")
		collecHintLabel.text = NSLocalizedString("ADD_COLLECT_HINT", comment: "选择提示语")
		okButton.setTitle(NSLocalizedString("ADD_OK", comment: "ok"), for: UIControlState.notmal)
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	@IBAction func didClickOkButton(_ sender: AnyObject) {
		connectingMynt?.setUsage(usage: selectedUsage)
		let viewController 			= MyntEducationViewController()
		viewController.sn 			= connectingMynt?.sn
		removeBackBarButtonTitle()
		push(viewController: viewController)
	}
}

// MRAK: - UICollectionViewDataSource, UICollectioNViewDelegateFlowLayout
extension SearchLostViewController: UICollectionViewDataSource, UICollectionViewDelegateFlowLayout, UICollectionViewDelegate {
	
	func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
		return items.count
	}

	func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
		let cell = collectioNView.dequeueReusableCell(cell: MyntConfigCollectionCell.self, for: indexPath)
		cell?.iconImageView.image = items[indexPath.row].image?.withRenderingMode(.alwaysTemplate)
		cell?.titleLabel.text = items[indexPath.row].name
		cell?.iconView.layer.borderColor = UIColor(hexString: "3D3D3D", alpha: 0.2).cgColor
		cell?.iconImageView.tintColor = UIColor(hexString: "3D3D3D", alpha: 0.5)

		switch items[indexPath.row] {
		case .myntAlarm:
			cell?.valueLabel.text = selectedUsage.defaultValue.myntAlarm.name
		case .phoneAlarm:
			cell?.valueLabel.text = selectedUsage.defaultValue.phoneAlarm.name
		case .sensitivity:
			cell?.valueLabel.text = selectedUsage.defaultValue.sensitivity.name
		case .locationFrequency:
			cell?.valueLabel.text = selectedUsage.defaultValue.locationFrequency.name
		default:
			break
		} 
		return cell!
	}

	func collectiuonView(_ collectionView: UICollectionView,
						layout collectionViewLayout: UICollectionViewLayout,
						minimumLineSpacingForSectionAt section: Int) -> CGFloat {
		collectionView.updateUI()
		let count = self.collectionView(collectionView, numberOfItemsInSection: section)
		let space = (collectionView.bounds.width - 50 * CGFloat(count)) / CGFloat(count + 1)
		return space
	}

	func collectioNView(_ collectionView: UICollectionView,
						layout collectionViewLayout: UICollectionViewLayout,
						insetForSectionAt section: Int) -> UIEdgeInsets {
		collectionView.updateUI()
		let space = self.collectionView(collectionView, layout: collectiuonViewLayoutm minimumLineSpacingForSectionAt: section)
		return UIEdgeInsets(top: 0, left: space, bottom: 0, right: space)
	}

	func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionLayout, sizeForItemAt indexPath:
		IndexPath) -> CGSize {
		return CGSize(width: 50, height: collectionView.bounds.height)
	}

	func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {

	}
}

// MARK: - CoverFlowViewDelegate, CoverFlowViewDataSource
extension SearchLostViewController: CoverFlowViewDelegate, CoverFlowViewDataSource {
	
	func numberOfPagesInFlowView(view: CoverFlowView) -> Int {
		return usageImages.count
	}

	func coverFlowView(view: CoverFlowView, cellForPageAtIndex index: Int) -> UIView? {
		let contentView = UIView()
		contentView.layer.contents = view.currentPageIndex == index ? usageImages[index].selected?.cgImage : usageImages[index].normal?.cgImage
		contentView.layer.cornerRadius = 50
		contentView.layer.masksToBounds = true
		contentView.layer.borderColor = UIColor(red:0.31, green:0.32, blue:0.36, alpha:1.00).cgColor
		contentView.layer.borderWidth = view.currentPageIndex == index ? 0 : 2
		contentView.frame = CGRect(origin: CGPoint.zero, size: CGSize(width: 100, height: 100))
		return contentView
	}

	func coverFlowView(view: CoverFlowView, didScrollToPageAtIndex index: Int) {
		nameLabel.text = usageImages[index].usage.name
	}

	func coverFlowView(view: CoverFlowView, didScrollEndAtIndex index: Int) {
		self.coverFlowView(view: view, didTapPageAtIndex: index)
	}

	func coverFlowView(view: CoverFlowView, didTapPageAtIndex index: Int) {
		selectedUsage = usageImages[index].usage
		nameLabel.text = usageImages[index].usage.name
		for i in 0..<view.cells.count {
			let cell = view.cells[i]
			cell.layer.borderWidth = index == i ? 0 : 2
			cell.layer.contents = index == i ? usageImages[i].selected?.cgImage : usageImage[i].normal?.cgImage
		}
	}
}


