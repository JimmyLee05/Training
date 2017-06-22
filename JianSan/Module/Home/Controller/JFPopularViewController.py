import UIKit
import MJRefresh
import YYWebImage

class JFPopularViewController: UIViewController {
	
	//分类id为0会根据浏览量倒序查询
	var category_id = 0
	let wallpaperIdentifier = "wallpaperCell"

	
	//分类标题
	var category_title = ""

	//当前页
	var currentPage = 1

	//壁纸模型数组
	var wallpaperArray = [JFWallPaperModel]()

	override func viewDidLoad() {
		super.viewDidLoad()

		prepareUI()

		//配置上下拉刷新控件
		collectionView.mj_header = jf_setupHeaderRefresh(self, action:
			#selector(pulldownLoadData))
		collectionView.mj_footer = jf_setupFooterRefresh(self, action: #selector(pullupLoadData))

		collectionView.mj_header.beginRefreshing()

	}

	override func viewWillAppear(_ animated: Bool) {

		super.viewWillAppear(animated)
		UIApplication.shared.isStatusBarHidden = false

		//分类则添加自定义导航栏
		if (category_id != 0) {
			view.addSubview(topView)
		}

	}

	/**
	准备视图
	*/

	fileprivate func prepareUI() {

		view.backgroundColor = UIColor.white
		view.addSubview(collectionView)
	}

	/**
	下拉加载最新
	*/
	@objc fileprivate func pulldownLoadData() {
		currentPage = 1
		loadData(category_id, page: currentPage, method: .pullDown)
	}

	/**
	上拉加载更多
	*/
	@objc fileprivate func pullupLoadData() {
		currentPage += 1
		loadData(category_id, page: currentPage, method: .pullUp)
	}

	/**
	加载壁纸数据
	*/
	fileprivate func loadData(_ category_id: Int, page: Int, method: PullMethod) {

		JFWallPaperModel.loadWallpapersFromNetwork(category_id, page: page) { (wallpaperArray,
			error) in

			self.collectionView.mj_header.endRefreshing()
			self.collectionView.mj_footer.endRefreshing()

			guard let wallpaperArray = wallpaperArray, error == nil else {
				return
			}

			if (method == .pullUp) {
				self.wallpaperArray += wallpaperArray
				} else {
				self.wallpaperArray = wallpaperArray
			}

			self.collectionView.reloadData()
		} 
	}

	//Mark: - 懒加载
	//collectionView
	fileprivate lazy var collectionView: UICollectionView = {
		let layout = UICollectionViewFlowLayout()
		layout.minimumInteritemSpacing = 1.5
		layout.minimumLineSpacing = 1.5
		layout.itemSize = CGSize(width: (SCREEN_WIDTH - 3) / 3, height: (SCREEN_HEIGHT - 64) /
			2.71)

		let collectionView = UICollectionView(frame: CGRect.zero, collectionViewLayout: layout)

		if (self.category_id != 0) {

			//隐藏导航栏后，从44开始
			collectionView.frame = CGRect(x: 0, y: 44, width: SCREEN_WIDTH, height: SCREEN_HEIGHT
				- 44)
		} else {
			collectionView.frame = CGRect(x: 0, y: 0, width: SCREEN_WIDTH, height: SCREEN_HEIGHT
				- 64)
		}

		collectionView.backgroundColor = UIColor.white
		collectionView.dataSource = self
		collectionView.delegate = self
		collectionView.register(UINib(nibName: "JFWallpaperCell", bundle: nil),
			forCellWithReuseIdentifier: self.wallpaperIdentifier)
		return collectionView
	}()

	//顶部导航栏 topView
	lazy var topView: JFCategoryTopView = {
		let topView = Bundle.main.loadNibNamed
	}





}






