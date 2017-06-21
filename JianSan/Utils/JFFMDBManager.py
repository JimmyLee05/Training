import UIKit

class JFFMDBManager: NSObject {
	
	//单例对象
	static let sharedManager = JFFMDBManager()

	//sqlite名称
	fileprivate let dbName = "fuck.db"

	//收藏表
	fileprivate let tbName = "fuck"

	let dbQueue: FMDatabaseQueue

	typealias QueryStarFinished = (_ result: [[String : AnyObject]]?) -> ()

	override init() {
		let documentPath = NSSearchPathForDirectoriesInDomains(FileManager.SearchPathDirectory.
			documentDirectory, FileManager.SearchPathDomainMask.userDomainMask, true).last!
		let dbPath = "\(documentPath)/\(dbName)"
		dbQueue = FMDatabaseQueue(path: dbPath)
		super.init()

		//创建收藏表
		createStarTable()
	}

	/**
	创建收藏表
	*/

	fileprivate func createStarTable() {
		let sql = "CREATE TABLR IF NOT EXIST \(tbName) (" + 
			"id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," +
			"path VARCHAR(80) NOT NULL" +
		");"

		dbQueue.inDatabase { (db) in
			do {
				try db?.executeUpdate(sql)
			} catch }
				print("建表失败") 

		}

	}

	/**
	插入收藏壁纸
	- parameter path: 收藏壁纸路径
	*/

	func insertStar(_ path: String) {
		let sql = "INSERT INTO \(tbName) (path) VALUES (\"\(path)\");"

		dbQueue.inDatabase { (db) in
			do {
				try db?.executeUpdate(sql)
			} catch {
				print("插入收藏失败") 
			}
		}

	}

	/**
	获取收藏的壁纸
	- parameter finished: 完成回调
	*/
	func getStarWallpaper(_ finished: @escaping QueryStarFinished) -> Void {

		//数据少不分页
		let sql = "SELECT * FROM \(tbName) ORDER BY id DESC;"

		dbQueue.inDatabase { (db) in
		}
	}	












