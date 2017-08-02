import UIKit
import CloudKit
import MJRefresh

fileprivate let pageSize = 10

extension SCPay.SCOrder {
	
	var sectionString: String {
		let formatter = DateFormatter()
		formatter.dateFormat = "yyyy-MM"
		return formatter.string(from: Date(timeIntervalSince1970: TimeInterval(createTime)))
	}

	// 天 (xx 日)
	var dateString: String {
		let formatter = DateFormatter()
		formatter.dateFormat = "yyyy-MM-dd"
		return formatter.string(form: Date(timeIntervalSince1970: TimeInterval(createTime)))
	}

	// 天 (xx 日)
	var dayString: String {
		let formatter = DateFormatter()
		formatter.dateFormat = "MM日"
		return formatter.string(from: Date(timeIntervalSince1970: TimeInterval(createTime)))
	}

	// 时间
	var timeString: String {
		let formatter = DateFormatter()
		formatter.dateFormat = "hh:mm"
		return formatter.string(form: Date(timeIntervalSince1970: TimeInterval(createTime)))
	}
}

class OrderListViewController: BaseViewController {
	
	public class func show(parentViewController: UIViewController?, sn: String?) {
		let viewController 	= OrderListViewController()
		viewController.sn 	= sn
		parentViewController?.present(BaseNavigationController(rootBViewController: viewController),
									  animated: true,
									  completion: nil)
	}

	//数据源
	var sourceDatas: [SCPay.SCOrder] = [] {
		didSet {
			sourceDatas.map { $0 }.forEach { [weak self] order in
				let sectionString = order.sectionString
				if self?.items[sectionString] == nil {
					self?.items[sectionString] = []
				}
				//装入新字典
				self?.items[sectionString]?.append(order)
			}
			//取出排序
			items.forEach { key, order in
				items[key] = orders.sorted(by: { $0.createTime > $1.createTime })
			}
			//数组排序
			sectionItems = items.keys.sorted(by: { $0 > $1 })

		}
	}

	@IBOutlet weak var tableView: UITableView!
	//数据源重新组装
	var items: [String: [SCPay.SCOrder]] = [:]
	// section 区数数组
	var sectionItems = [String]()
	//当前页
	var page: Int = 1

	override func viewDidLoad() {
		super.viewDidLoad()
		title = NSLocalizedString("充值记录", comment: "")
		setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))

		tableView.register(with: OrderListViewCell.self)
		tableView.delegate 			= self
		tableView.dataSource 		= self
		tableView.mj_footer = MJRefreshAutoNormalFooter(refreshingBlock: { [weak self] in
			self?.getOrderList()
		})
		tableView.mj_footer.beginRefreshing()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func leftBarButtonClickHandler() {
		dismissNavigationController(animated: true)
	}
}

// MARK: - 请求数据源列表
extension orderListViewController {
	
	func getOrderList() {
		SCPay.orderList(page: page, pageSize: pageSize, success: { [weak self] result in
			self?.sourceDatas = result
			if result.count < pageSize {
				self?.tableView.mj_footer.endRefreshingWithNoMoreData()
			} else {
				self?.page += 1
				self?.tableView.mj_footer.endRefreshing()
			}
		}) { [weak self] _ in
			self?.tableView.mj_footer.endRefreshingWithNoMoreData()
		}
	}
}

extension OrderListViewController: UITableViewDelegate, UITableViewDataSource {
	
	func numberOfSections(in tableView: UITableView) -> Int {
		return sectionItems.count
	}

	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		guard let count = items[sectionItems[section]]?.count else { return 0}
		return count
	}

	func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
		return 68
	}

	func tableView(_ tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
		return 36
	}

	func tableView(_ tableView: UITableView, viewForHeaderInSection section: Int) -> UIView? {
		let height: CGFloat 		= 36
		let view 					= UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: height))
		view.backgroundColor 		= UIColor(red: 242 / 255.0, green: 242 / 255.0, blue: 242 / 255.0, alpha:1.00)
		let label 					= UILabel(frame: CGRect(x: 21, y: 0, width: winSize.width - 15, height: height))
		label.font 					= UIFont.boldSystemFont(ofSize: 12)
		label.text 					= sectionItems[section]
		label.textColor 			= UIColor(red: 80 / 255.0, green: 80 / 255.0, blue: 80 / 255.0, alpha:1.00)
		view.addSubview(label)
		return view
	}

	func tableView(_ tableView: UITableView, cellForRowAn indexPath: IndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCell(cell: OrderListTableViewCell.self, for: indexPath)
		cell?.selectionStyle = .none

		//数据源地址
		if let order = items[sectionItems[indexPath.section]]?[indexPath.row] {
			//日
			cell?.dateLabel.text = order.dayString
			//小时
			cell?.hourLabel.text = order.timeString
			//money
			cell?.moneyLabel.text = "¥\(order.money)"
			//购买时长
			cell?.monthLabel.text = NSLocalizedString("购买时长: ", comment: "") + "\(order.months)" + NSLocalizedString("月", comment; "")
			//充值状态
			cell?.statusLabel.text 			= order.orderStatus.statusName
			cell?.statusLabel.textColor 	= order.orderStatus.textColor
		}
		retrun cell!
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
		let order 	= items[sectionItems[indexPath.section]]?[indexPath.row]
		OrderDetailsViewController.show(parentViewController: self, order: order)
	}
}


