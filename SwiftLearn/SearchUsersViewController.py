import UIKit
import SCloudKit

class SearchUsersViewController: BaseViewController {
	
	@IBOutlet weak var resultLabel: UILable!
	@IBOutlet weak var searchBar: UISearchBar!
	@IBOutlet weak var tableView: UITableView!

	var shareFriendSuccessHandler: (() -> Void)?

	var existFriends = [SCFriend]()
	// 搜索的匹配数据
	var friends = [SCFriend]() {
		didSet {
			resultLabel.isHidden = !friends.isEmpty
			tableView.reloadData()
		}
	}

	override func viewDidLoad() {

		super.viewDidLoad()
		title = MTLocalizedString("GPS_SHARE_ADD", comment: "添加共享")
		setLeftBarButtonItem(image: Resource.Image.Navigation.close)

		tableView.register(with: MTImageTableViewCell.self)
		tableView.tableHeaderView = UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: 0))
		tableView.delegate 		= self
		tableView.dataSource 	= self

		resultLabel.text 		= MTLocalizedString("GPS_ADD_RESULT", comment: "搜索结果")
		resultLabel.isHidden 	= true

		searchBar.placeholder 	= MTLocalizedString("GPS_SEARCH_USER", comment: "输入用户名 ／ 邮箱")
		searchBar.delegate 		= self
		view.supportHideKeyBoard()
		tableView.reloadData()
	}

	


}

















