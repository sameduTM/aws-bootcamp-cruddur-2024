import './ProfileAvatar.css';

export default function ProfileAvatar(props) {
    if (props.id !== undefined) {
        const backgroundImage = `url("https://assets.codeken.me/avatars/${props.id}.jpg")`;
        const styles = {
            backgroundImage,
            backgroudSize: 'cover',
            backgroundPostition: 'center',
        }
        return (
            <div className='profile-avatar' style={styles}></div>
        );
    }
}