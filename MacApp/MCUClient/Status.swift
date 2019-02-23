//
//  Status.swift
//  MCUClient
//
//  Created by Anatoly Kasyanov on 2/14/19.
//

import Foundation

class StatusAPI {
    
    let restApiKey = "B0E06E82-FA42-D6E5-FF3A-95B227096C00"
    let applicationID = "32F23448-DA51-7F84-FFC7-47289F758100"
//    let baseURL = "https://api.backendless.com/32F23448-DA51-7F84-FFC7-47289F758100/B0E06E82-FA42-D6E5-FF3A-95B227096C00/data/events"
//    let baseURL = "http://192.168.31.116"
    let baseURL = "http://192.168.4.1"
   
    func makeGetCall(completion: @escaping (String) -> Void) {

        let statusEndpoint = baseURL

        // Set up the URL request
        guard let url = URL(string: statusEndpoint) else {
            print("Error: cannot create URL")
            return
        }
        let urlRequest = URLRequest(url: url)
        
        // set up the session
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 2
        let session = URLSession(configuration: config)
        
        // make the request
        let task = session.dataTask(with: urlRequest) {
            (data, response, error) in
            // check for any errors
            guard error == nil else {
                completion("false")
                print("error calling GET")
                print(error!)
                return
            }
            // make sure we got data    
            guard let responseData = data else {
                completion("false")
                print("Error: did not receive data")
                return
            }
            // parse the result as JSON, since that's what the API provides
            do {
                guard let status = try JSONSerialization.jsonObject(with: responseData, options: [])
                    as? [String: Any] else {
                        completion("false")
                        print("error trying to convert data to JSON")
                        return
                }
                // now we have the todo
                // let's just print it to prove we can access it
//                print("Data: " + status.description)
                
                // the todo object is a dictionary
                // so we just access the title using the "title" key
                // so check for a title and print it if we have one
//                guard let isOpen = status["isOpen"] as? String else {
                guard let isOpen = status["isOpen"] as? String else {
                    completion("false")
                    print("Could not get isOpen key from JSON")
                    return
                }
                
                completion(isOpen)
//                print("isOpen: \(isOpen)")

            } catch  {
                print("error trying to convert data to JSON")
                return
            }
        }
        task.resume()
    }
}
