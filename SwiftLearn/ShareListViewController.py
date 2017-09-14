import UIKit
import MYNTKit
import SCloudKit

class ShareListViewController: BaseViewController {
	
	enum CellType {
		case coverflow
		case empty
		case line
		case permissions

		var height: CGFloat {

			switch self {
			case .coverflow:
				return 220
			case .line:
				return 0.5
			case .empty:
				return 30
			case .permissions:
				return 60
			}
		}
	}

	
}