import UIKit

class JFCategoryCell: UICollectionViewCell {
	
	@IBOutlet weak var categoryImageView: UIImageView!

	var model: JFCategoryModel? {
		didSet {
			categoryImageView.image = UIImage(named: "category_\(model?.alias ?? "")")?.
				redrawImage(size: categoryImageView.bounds.size)
		}
	}
}