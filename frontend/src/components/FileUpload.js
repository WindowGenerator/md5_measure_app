import React, { Fragment, useState } from 'react';
import Message from './Message';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState('');
  const [filename, setFilename] = useState('Choose File');
  const [taskId, setTaskId] = useState('Type Task ID');
  const [hashedFileText, setHashedFileText] = useState(null);
  const [message, setMessage] = useState('');

  const onChangeFileField = e => {
    setFile(e.target.files[0]);
    setFilename(e.target.files[0].name);
  };

  const onChangeTaskIdField = e => {
    setTaskId(e.target.value);
  };

  const onSubmitComputeHash = async e => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('upload_file', file);

    try {
      const res = await axios.post("http://localhost:8000/api/v1/files/compute/hash", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setMessage(`Created task with id: ${res.data.task_id}`);

    } catch(err) {
      if(err.response.status === 500) {
        setMessage('There was a problem witht he server');
      } else {
        setMessage(err.response.data.msg);
      }
      return;
    }
  }

  const onSubmitGetComputedHash = async e => {
    e.preventDefault();
    try {
      const res = await axios.get(`http://localhost:8000/api/v1/files/compute/hash?task_id=${taskId}`);

      setHashedFileText(textFromHashedFile(res.data));
    } catch(err) {
      return;
    }
  }

  const textFromHashedFile = (hashedFile) => {
    return (
      <div>
        <p>Task ID: {hashedFile.task_id}</p>
        <p>Status: {hashedFile.status}</p>
        <p>Hash Value: {hashedFile.hash_value}</p>
        <p>Hash Type: {hashedFile.hash_type}</p>
      </div>
    );
  }

  return (
    <Fragment>
      <div class="d-grid gap-3">
        <h2 className="text-center p-4">Please choose your file:</h2>
        { message ? <Message msg={ message } /> : null }
        <form onSubmit={onSubmitComputeHash}>
          <div className="custom-file mb-4">
            <input
              type="file"
              className="custom-file-input"
              id="customFile"
              onChange={onChangeFileField}
            />
            <label className='custom-file-label' htmlFor='customFile'>
              {filename}
            </label>
          </div>

          <input
            type="submit"
            value="Upload"
            className="btn btn-primary btn-block mt-4"
          />
        </form>
        <h2 className="text-center p-4">Please input task_id:</h2>
        <form onSubmit={onSubmitGetComputedHash}>
          <div className="input-group mb-3">
            <div className="input-group-prepend">
              <span className="input-group-text" id="basic-addon1">UUID:</span>
            </div>
            <input
              type="text"
              className="form-control"
              aria-describedby="basic-addon1"
              id="get-task-id-input"
              onChange={onChangeTaskIdField}
            />
          </div>

          <input
            type="submit"
            value="Get Task"
            className="btn btn-primary btn-block mt-4"
          />
        </form>
        { hashedFileText ? <Message msg={ hashedFileText } /> : null }
      </div>
    </Fragment>
  );
};

export default FileUpload;
