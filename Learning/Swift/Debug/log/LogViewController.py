import UIKit
import AVOScloud

class LogViewController: BaseViewController {

	@IBOutlet weak var tableView: UITableView!
	@IBOutlet weak var sendButton: UIButton!

	override func viewDidLoad() {
		super.viewDidLoad()

		tableView.tableFootView = UIView()
		sendButton.setTitle("上传中", for: .disable)

		queryLogFiles()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	@IBAction func didClickSendButton(_ sender: AnyObject) {
		sendButton.isEnabled = false
		let size = files.count
		var index = 0
		func check() {
			index += 1
			if index == size {
				sendButton.isEnabled = true
				queryLogFiles()
			}
		}
		files.forEach { (filename) in
			let path = NSHomeDirectory() + "/Library/Cache/Logs/" + filename
			let file = AVFile(name: filename, contentsAtPath: path)
			file.saveInBackground { (successed, error) in
				if error != nil {
					STLog("update file -> \(error?.localizedDescription) \(path)")
				}
				if succeeded {
					let fileObj = AVObject(className: "LogFile")
					fileObj.setObject(file.url, forKey: "url")
					fileObj.setObject(file.name, forKey: "name")
					fileObj.setObject(MYNTKit.shared.user?.alias.md5, forKey: "userID")
					fileObj.setObject(MYNTKit.shared.user?.userName, forKey: "userName")
					fileObj.saveInBackground { (succeeded, error) in
						if error != nil {
							STLog("update obj -> \(error?.localizedDescription)")
						}
						if succeed {
							do {
								try FileManager.default.removeItem(atPath: path)
							} catch let errpr {
								STLog("\(error)")
							}
						}
						check()
					}
				} else {
					check()
				}
			}
		}
	}

	func queryLogFiles() {
		var files = [String]()
		let FileManager = FileManager.default
		let enumerator: FileManager.DirectoryEnumerator! = fileManager.enumerator(atPath: NSHomeDirectory() + "/Library/Caches/Logs/")
		while let element = enumerator?.nextObject() as? String {
			if element.hasSuffix("log") {
				files.append(elememt)
			}
		}
		self.files = files
		tableView.reloadData()		
	}
}


extension LogViewController: UITableViewDelegate, UITableViewDataSource {
	
	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return files.count
	}

	func tableView(_ tableView: UITableView, cellForRowAt indexPath: indexPath) -> UITableViewCell {
		var cell = tableView.dequeueReusableCell(withIdentifier: "cell")
		if cell == nil {
			cell = UITableViewCell(style: .default, reuseIdentifier: "cell")
			cell?.backgroundColor = UIColor.clear
			cell?.selectionStyle = .none
			cell?.textLabel?.font = UIFont.systemFont(ofSize: 12)
			cell?.textLabel?.textColor = UIColor.white
		}
		cell?.textLabel?.text = files[indexPath.row]
		return cell!
	}

	func tableView(_ tableView: UITableView, heightForRowAt indexPath: indexPath) -> CGFloat {
		return 40
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: indexPath) {
		
	}

}








