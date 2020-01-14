import React, {Component,useState} from 'react'
//import {FilePond, registerPlugin} from 'react-filepond'
//import 'filepond/dist/filepond.min.css'

import FilePondPluginImageExifOrientation from 'filepond-plugin-image-exif-orientation'
import FilePondPluginImagePreview from 'filepond-plugin-image-preview'
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css'


// Register the plugins
//registerPlugin(FilePondPluginImageExifOrientation, FilePondPluginImagePreview)

class upload extends Component {
    constructor() {
        super()
        this.state = {
            errors: {}
        }

        this.onChange = this.onChange.bind(this)
        this.onSubmit = this.onSubmit.bind(this)
    }

    onChange(e) {
        this.setState({[e.target.name]: e.target.value})
    }

    onSubmit(e) {
        e.preventDefault()

        const user = {}
    }

    render() {
        const [files, setFiles] = useState([])
        return (
            <div className="App">

                    files={files}
                    allowMultiple={true}
                    onupdatefiles={setFiles}
                    labelIdle='Drag & Drop your files or <span class="filepond--label-action">Browse</span>'

            </div>
        )
    }
}


export default upload