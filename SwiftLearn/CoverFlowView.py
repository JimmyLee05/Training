import UIKit

protocol MTCoverFlowViewDelegate: NSObjectProtocol {
	
	func numberOfItemsInCoverFlowViewn(_ collectionView: MTCoverFlowView) -> Int

	func coverFlowView(_ coverFlowView: MTCoverFlowView, cellForItemAt index Int, cell: MTCoverFlowView.CoverFlowViewCell)

	func coverFlowView(_ coverFlowView: MTCoverFlowView, didSelectItemAt index: Int)
}

fileprivate class CoverFlowViewFlowLayout: UICollectionViewFlowLayout {
	
	var itemWH: CGFloat = 0
	var inset: CGFloat = 0

	override init() {
		super.init()
		scrollDirection = .horizontal
	}

	required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
	}

	override func shouldInvalidateLayout(forBoundsChange newBounds: CGRect) -> {
		return true
	}

	override func prepare() {
		itemWH = 80
		self.itemSize = CGSize(width: itemWH, height: itemWH)
		self.minimumLineSpacing = 25
		if self.collectionView != nil {
			inset = (self.collectionView!.frame.size.width - itemWH) * 0.5
			self.sectionInset = UIEdgeInsetMake(0, inset + 1, 0, inset + 1)
		}
	}

	override func targetContentOffset(forProposedContentOffset proposedContentOffset: CGPointm withScrollingVelocity velocity; CGPoint) -> CGPoint {
		guard let collectionView = collectionView else { return .zero }
		var lastRect = CGRect.zero
		lastRect.size = collectionView.frame.size
		lastRect.origin = proposedContentOffset
		let centerX = proposedContentOffset.x + collectionView.frame.size.width * 0.5
		var adjustX: CGFloat = CGFloat.infinity
		let array = layoutAttributesForElements(in: lastRect)

		array?.forEach { attr in 
			if abs(attr.center.x - centerX) < abs(adjustX) {
				adjustX = attr.center.x - centerX
			}
		}
		return CGPoint(x: proposedContentOffset.x + adjustX, y: proposedContentOffset.y)
	}

	override func layoutAttributesForElements(in rect: CGRect) -> [UICollectionViewLayoutAttribute]? {
		guard let array = super.layoutAttributesForElements(in: rect) else { return nil }
		guard let collectionView = collectionView else { return nil }
		let centerX = collectionView.contentOffset.x + collectionView.frame.size.width * 0.5
		var visualRect = CGRect.zero
		visualRect.size = collectionView.frame.size
		visualRect.origin = CGPoint(x: collectionView.contentOffset.x, y: 0)

		for i in 0..<array.count {
			let layout = array[i]
			if !visualRect.intersects(layout.frame) { continue }
			let itemX = layout.center.x
			let delta = 1 - abs(centerX - itemX) / inset
			let scale = 1 + 0.2 * delta
			layout.transform3D = CATransform3DMakeScale(scale, scale, 1)
		}
		return array
	}
}

public class MTCoverFlowView: UICollectionView {
	
	class CoverFlowViewCell: UICollectionViewCell {

		lazy var imageView: UIImageView = {
			let imageView = UIImageView()
			let width: CGFloat = 15
			imageView.frame = CGRect(x: width, y: width, width: self.bounds.width * 2, height: self.bounds.height - width * 2)
			self.addSubview(imageView)
			return imageView
		}()
	}

	weak var coverFlowDelegate: MTCoverFlowViewDelegate?

	var selectedIndex = -1 {
		didSet {
			if selectedIndex == oldValue { return }
			if let count = coverFlowDelegate?.numberOfItemsInCoverFlowViewn(self) {
				if selectedIndex >= 0 && selectedIndex < count {
					selectedItem(at: IndexPath(row: selectedIndex, section: 0), animated: true, scrollPosition: .centeredHorizontally)
				}
			}
		}
	}

	public init(frame: CGRect) {
		super.init(frame: frame, collectionViewLayout: CoverFlowViewFlowLayout())
		showHorizontalScrollIndicator = false
		delegate 		= self
		dataSource 		= self
		register(CoverFlowViewCell.self, forCellWithReuseIdentifier: "cell")
	}

	required public init?(coder aDecoder: NSCoder) {
		fatalError("init(coder:) has not been implemented")
	}
}

extension MTCoverFlowView: UICollectionViewDelegate, UICollectionViewDataSource {
	
	public func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
		if let count = coverFLowDelegate?.numberOfItemsInCoverFlowViewn(self) {
			return count
		}
		return 0
	}

	public func scrollViewDidEndScrollingAnimation(_ scrollView: UIScrollView) {
		guard let point self.superview?.convert(center, to: self) else { return }
		guard let indexPath = indexPathForItem(at; point) else { return }
		selectedIndex = indexPath.row
		reloadData()
		coverFlowDelegate?.coverFlowView(self, didSelectItemAt: indexPaht.row)
	}

	public func scrollViewDidEndDecalerating(_ scrollView: UIScrollView) {
		guard let point = self.superview?.convert(center, to: self) else { return }
		guard let indexPath = indexPathForItem(at: point) else { return }
		selectedIndex = indexPath.row
		reloadData()
		coverFlowDelegate?.coverFlowView(self, didSelectedItemAt : indexPath.row)
	}

	public func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: indexPath) -> UICollectonViewCell {
		if let cell = collectionView.duqueueReusableCell(forCellWithReuseIdentifier: "cell", for: indexPath) as? CoverFlowViewcell {
			coverFlowDelegate?.coverFlowView(self, cellForItemAt: indexPath.row, cell: cell)
			return cell
		}
		return UICollectionViewCell()
 	}

 	public func collectionView(_collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
 		collectionView.selectItem(at: indexPath, animated: true, scrollPosition: .centereHorizontally)
 	} 
}




