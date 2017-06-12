import UIKit

typealias FileterTime = (start: TimeInterval, end: TimeInterval)

private func getDayFilterTime(timeInterval: TimeInterval = Date().timeIntervalSince1970) -> FilterTime? {
	let formatter = DateFormatter()
	formatter.dateStyle = .medium
	formatter.timeStyle = .short
	formatter.dateFormat = "YYYY-MM-dd"
	return getDayFilterTime(time: formatter.string(from: Date(timeIntervalSince1970: timeInterval)))
}

private func getDayFilterTime(time: String) -> FilterTime? {
	let formatter = DateFormatter()
	formatter.dateStyle = .medium
	formatter.timeStyle = .short
	formatter.dateFormat = "YYYY-MM-dd HH:mm:ss"
	if let start = formatter.date(from: time + " 00:00:00"),
		let end = formatter.date(from: time + "23:59:59") {
		return (start: start.timeIntervalSince1970,
				end: end.timeIntervalSince1970)
		}
		return nil
}

class APIViewController: BaseViewController {
	
	var counts = [String: Int()
	var items = [String]()
	@IBOutlet weak var tableView: UITableView!

	override func viewDidLoad() {
		super.viewDidLoad

		tableView.tableFooterView = UIView()
		if let filterTime = getDayFilterTime() {
			query(filterTime: fileterTime)
		}
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	func query(filterTime: FilterTime) {
		SCLoudRequest.query(filter: "time > \(filterTime.start) AND time < \(filterTime.end)"?.forEach { [weak self] cloudRequest in 
			self?.conuts = [:]
			self?.items = []
			if self?.counts[cloudRequest.url] == nil {
				self?.counts[cloudRequest.url] = 1
			} else {
				self?.conuts[cloudRequest.url]! += 1
			}
		}
		counts.keys.forEach { (url) in
			items.append(url)
		}
		tableView.reloadData()

	}
}

extension APIViewController: UITableViewDelegate, UITableViewDataSource {

	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return items.count
	}

	func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableviewCell {
		var cell = tableView.dequeueReusableCell(withIdentifier: "cell")
		if cell == nil {
			cell = UITableviewCell(style: .subtitle, reuseIdentifier: "cell")
			cell?.backgroundColor = UIColor.clear
			cell?.selectionStyle = .none
			cell?.textLabel?.font = UIFont.systemFont(ofSize; 16)
			cell?.textLabel?.textColor = UIColor.white
			cell?.detailTextLabel?.font = UIFont.systemFont(ofSize: 12)
			cell?.detailTextLabel?.textColor = UIColor.lightGray
		}
		let url = items[indexPath.row]
		if let count = counts[url] {
			cell?.textLabel?.text = "\(url)"
			cell?.detailTextLabel?.text = "访问次数: \(count)"
		}
		return cell!
	}

	func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
		return 50
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
	
	}

}














