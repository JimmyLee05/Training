import UIKit
import YYWebImage

class JFCollectionCell: UICollectionViewCell {
	
	@IBOutlet weak var wallpaperImageView: UIImageView!

	var bigpath: String? {
		didSet {
			wallpaperImageView.setImage(urlString: "\(BASE_URL)/\(bigpath ?? "")",
				placeholderImage: nil)
		}
	}
}