import React, {ChangeEvent, useState} from "react";
import {Button, Input} from "antd";
import Modal from "antd/es/modal/Modal";
import {ModalFooter} from "./ModalFooter/ModalFooter";
import {ModalBody} from "./ModalBody/ModalBody";
import {DeleteOutlined} from "@ant-design/icons";
import css from './ModalQuiz.module.css';
import {IQuizGroup} from "../../api/quiz.interface";
import {useImmer} from "use-immer";
import {updateQuizGroup} from "../../api/quiz.api";
import {getQuizGroupsFromRequest} from "../../store/slices/quizGropSlice";
import {useAppDispatch} from "../../hooks/reduxHooks";

export const ModalQuiz = (props: {
    quizGroup: IQuizGroup;
    deleteHandler: () => void;
}): JSX.Element => {
    const {quizGroup, deleteHandler} = props;
    const [open, setOpen] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const [product, updateProduct] = useImmer<IQuizGroup>(quizGroup);
    const dispatch = useAppDispatch();

    const showModal = () => {
        setOpen(true);
    };
    const handleCancel = () => {
        setOpen(false);
    };
    const handleOk = () => {
        setLoading(true);
        updateQuizGroup(product).then(() => {
            setLoading(false);
            setOpen(false);
            dispatch(getQuizGroupsFromRequest());
        })

    };

    const handelInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        updateProduct(draft => {
            draft.title = event.target.value
        });
    };
    return (
        <>
            <div className={css.button_wrapper}>
                <Button type="primary" className={css.button} onClick={showModal}>
                    {product.title}
                </Button>
                <DeleteOutlined onClick={deleteHandler} className={css.remove}/>
            </div>
            <Modal
                className={css.modal}
                open={open}
                width={'60%'}
                title={<Input bordered={false} placeholder={'Add group title'} onChange={handelInputChange}
                              value={product.title}/>}
                onOk={handleOk}
                onCancel={handleCancel}
                footer={<ModalFooter handleCancel={handleCancel} loading={loading} handleOk={handleOk}/>}
            >
                <ModalBody quizGroup={product} updateProduct={updateProduct}/>
            </Modal>
        </>
    );
}