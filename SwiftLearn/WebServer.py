import UIKit
import GCDWebServers

class WebServer: NSObject, GCDWebUploaderDelegate {
	
	static let shared = WebServer()

	var webServer: GCDWebUploader?

	var isOpen = false

	private override init() {
		super.init()
	}

	func open(block: (Bool) -> Void) {
		let path = NSHomeDirectory()
		GCDWebUploader.setLogLevel(2)
		webServer = GCDWebUploader(uploadDirectory: path)
		webServer?.delegate = self
		webServer?.allowHiddenItems = true
		var msg = ""
		if webServer?.start() == true {
			if let url = webServer?.serverURL {
				if let url = url.absoluteString.substringWithRange(start: 0, length: url.absoluteString.length - 1),
					let port = webServer?.port {
					msg = "GCDWebServer running \(url):\(port)"
					isOpen = true
					block(false)
				} else {
					msg = "GCDWebServer not running!"
					block(false)
				}
			} else {
				msg = "GCDWebServer not running!"
				block(false)
			}
		} else {
			msg = "GCDWebServer not running!"
			block(false)
		}
		STLog(msg)

		let winSize = UIScreen.main.bounds.size
		let label = UILabel(frame: CGRect(x: 0, y: winSize.height - 20, width: winSize.width, height: 20))
		label.tag = 10000
		label.backgroundColor = UIColor(white: 0, alpha: 0.2)
		label.textColor = UIColor.white
		label.text = msg
		label.textAligment = .center
		label.font = UIFont.systemFont(ofSize: 8)
		UIApplication.shared.keyWindow?.addSubview(label)
		label.perform(#selector(UILabel.removeFromSuperview), with: nil, afterDelay: 20)
	}

	func close() {
		webServer?.stop()
		webServer = nil
		isOpen = false
	}

	func webUploader(_ uploader: GCDWebUploader!, didUploadFileAtPath path: String!) {
		STLog("[UPLOAD] %@", path)
	}

	func webUploader(_ uploader: GCDWebUploader!, didMoveItemFromPath fromPath: String!, toPath: String!) {
		STLog("[MOVE] %@ -> %@", fromPath, toPath)
	}

	func webUploader(_ uploader: GCDWebUploader!, didDeleteItemAtPath path: String!) {
		STLog("[DELETE] %@", path)
	}

	func webUploader(_ uploader: GCDWebUploader!, didCreateDirectoryAtPath path: String!) {
		STLog("[CREATE] %@", path)
	}
}

