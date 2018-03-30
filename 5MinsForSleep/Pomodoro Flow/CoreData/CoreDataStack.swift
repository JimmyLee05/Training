//
//  CoreDataStack.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/28.
//  Copyright © 2018年 Dan K. All rights reserved.
//

import CoreData

@available(iOS 10.0, *)
class CoreDataStack {

    static let persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "Pomodoro Flow")
        container.loadPersistentStores { (_, error) in
            if let error = error as NSError? {
                fatalError("Unresolved error \(error), \(error.userInfo)")
            }
        }
        return container
    }()

    static var context: NSManagedObjectContext { return persistentContainer.viewContext }

    class func saveContext () {
        let context = persistentContainer.viewContext

        guard context.hasChanges else {
            return
        }

        do {
            try context.save()
        } catch {
            let nserror = error as NSError
            fatalError("Unresolved error \(nserror), \(nserror.userInfo)")
        }
    }
}
