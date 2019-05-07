//
//  Status.swift
//  MCUClient
//
//  Created by Anatoly Kasyanov on 2/14/19.
//

import Foundation

class StatusAPI {

    var baseURL: String? //"http://192.168.31.116"
    var song: String?
    
    func readConfig() -> String {
        let homeDirURL = FileManager.default.homeDirectoryForCurrentUser.path
        let filePath = "\(homeDirURL)/tubzel.cfg"
        let dict = readJSONFromFile(filePath: filePath) as? Dictionary<String, Any>
        
        let urlValue = dict?["ip"] as? String
        baseURL = "http://\(urlValue!)"
        song = dict?["song"] as? String
        
        if let song = song {
            return song
        }
        return ""
    }
    
    func readJSONFromFile(filePath: String) -> Any? {
        var json: Any?
        if FileManager.default.fileExists(atPath: filePath) {
            do {
                let fileUrl = URL(fileURLWithPath: filePath)
                // Getting data from JSON file using the file URL
                let data = try Data(contentsOf: fileUrl, options: .mappedIfSafe)
                json = try? JSONSerialization.jsonObject(with: data)
            } catch {
                // Handle error here
            }
        }
        return json
    }
    
    func makeGetCall(completion: @escaping (String) -> Void) {

        // Set up the URL request
        guard let baseURL = baseURL, let url = URL(string: baseURL) else {
            print("Error: cannot create URL")
            return
        }
        let urlRequest = URLRequest(url: url)
        
        // set up the session
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 3
        
//        let session = URLSession(configuration: config)
        let session = URLSession(configuration: config)
        
        // make the request
        let task = session.dataTask(with: urlRequest) {
            (data, response, error) in
            // check for any errors
            guard error == nil else {
                completion("noConnection")
                print("error calling GET")
                print(error!)
                return
            }
            // make sure we got data    
            guard let responseData = data else {
                completion("noConnection")
                print("Error: did not receive data")
                return
            }
            // parse the result as JSON, since that's what the API provides
            do {
                guard let status = try JSONSerialization.jsonObject(with: responseData, options: [])
                    as? [String: Any] else {
                        completion("noConnection")
                        print("error trying to convert data to JSON")
                        return
                }
           
                // final result
                guard let isOpen = status["isOpen"] as? String else {
                    completion("noConnection")
                    print("Could not get isOpen key from JSON")
                    return
                }
                
                completion(isOpen)
                print("isOpen: \(isOpen)")

            } catch  {
                print("error trying to convert data to JSON")
                return
            }
        }
        task.resume()
    }
    
    func makePostRequest(song: String) {
        guard let baseURL = baseURL, let urlBaseStr = URL(string: baseURL) else {
            print("Error: cannot create URL")
            return
        }
        let urlWithParams = "\(urlBaseStr)?song=\(song)"
        let parameters = ["song": "starwars2"]
        
        //create the url with URL
        let url = URL(string: urlWithParams)! //change the url
        
        //create the session object
        let session = URLSession.shared
        
        //now create the URLRequest object using the url object
        var request = URLRequest(url: url)
        request.httpMethod = "POST" //set http method as POST
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted) // pass dictionary to nsdata object and set it as request body
        } catch let error {
            print(error.localizedDescription)
        }
        
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue("application/json", forHTTPHeaderField: "Accept")
        
        //create dataTask using the session object to send data to the server
        let task = session.dataTask(with: request as URLRequest, completionHandler: { data, response, error in
            
            guard error == nil else {
                return
            }
            
            guard let data = data else {
                return
            }
            
            do {
                print("response from server")
                //create json object from data
//                if let json = try JSONSerialization.jsonObject(with: data, options: .mutableContainers) as? [String: Any] {
//                    print(json)
//                    // handle json...
//                }
            } catch let error {
                print(error.localizedDescription)
            }
        })
        task.resume()
    }
}
